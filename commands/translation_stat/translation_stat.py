from github import Github, Repository, GithubObject
import json
import os
from threading import Lock
import discord
from discord import app_commands
from discord.app_commands import Choice
from contextlib import nullcontext
import re

g: Github = None
repo: Repository = None

# repo = g.get_repo("placeTW/website")
main_lang = "en"
json_matches: dict[str, list[str]] = {
    "translation.json": [r".*\/(title|blurb|desc)"],
    "art-pieces.json": [r".*"]
}


def check_file_include_rule(path: str) -> bool:
    return re.search("public\/locales\/.*\/(art-pieces\.json|translation\.json)", path)


def filename_rm_sector(filename: str, sectors: int) -> str:
    index = 0
    for i in range(sectors):
        index = filename.find("/", index + 1)
        if index == -1:
            raise IndexError(
                "Not enough sectors for string {}".format(filename)
            )
    return filename[index + 1:]


def handle_filename(filename: str, sectors: int) -> tuple[str, str]:
    filename = filename_rm_sector(filename, sectors)
    locale = filename[: filename.find("/")]
    filename = filename_rm_sector(filename, 1)
    return filename, locale


def generate_progress_str(percentage: float, size: int) -> str:
    slice = 1 / size
    return "[{}]".format(
        f"{'⬜' if slice * (it + 1) < percentage else '⬛'}"
        for it in range(size)
    )


class transfile_progress:
    def __init__(self, total_indexes=0, json_data={}):
        self.all_fields: dict[str, bool] = {}
        self.ready_indexes = int()
        self.total_indexes = (
            total_indexes if total_indexes else self.ready_indexes
        )
        if json_data:
            for key, value in json_data.items():
                self.all_fields[key] = value
        for _, value in self.all_fields.items():
            if value:
                self.ready_indexes += 1

    def progress_str_fwd(self) -> str:
        return generate_progress_str(self.ready_indexs / self.total_indexes, 10)

    def load_file(self, filename, json_data: dict) -> None:
        standards: list[list[str]] = []
        for item in json_matches[filename]:
            standards.append(item.split('/'))

        def match(iter: int, target: dict, pre_str="") -> None:
            nonlocal standards, self
            for key, value in target.items():
                for item in standards:
                    if re.match(key, item):
                        if iter + 1 == len(item):
                            self.all_fields[pre_str] = str(value)
                            break
                        pre_str += f"/{key}"
                        match(iter + 1, value, pre_str=pre_str)
                        break

        match(0, json_data)


# test = transfile_progress()
# with open("../../trans_data/zh/art-pieces.json", "r") as fff:
#     test.load_file("art-pieces.json", json.loads(fff.read()))
#
# print(test.all_fields)

# exit(0)


def write_data(
    locale: str,
    filename: str,
    full_path: str,
    commit_ref: str = GithubObject.NotSet,
) -> None:
    if filename not in json_matches.keys():
        return
    if not os.path.exists("trans_data/{}".format(locale)):
        os.makedirs("trans_data/{}".format(locale))
    with open("trans_data/{}/{}".format(locale, filename), "w+") as out:
        out.write(
            repo.get_contents(
                full_path, ref=commit_ref
            ).decoded_content.decode("utf-8")
        )


class locale_t:
    def __init__(self) -> None:
        self.owned_files: list[str] = None
        self.pr_files: list[str] = []
        self.pr_no: str = None
        self.mutex: Lock = Lock()

    def sync_pr_files(self, filenames: list[str] = None):
        if filenames:
            if self.owned_files:
                self.owned_files = list(set(self.owned_files) - set(filenames))
        self.pr_files = filenames

    def sync_master_files(self, filenames: list[str] = None):
        if filenames:
            if self.pr_files:
                self.pr_files = list(set(self.pr_files) - set(filenames))
        self.owned_files = filenames


trans_db_lock = Lock()
trans_db: dict[str, locale_t] = {}


def get_by_pr(locale_check: str, pr_no: int) -> None:
    pr = repo.get_pull(pr_no)
    pr_files_to_add: list[str] = []
    all_commits = pr.get_commits()
    for iter in reversed(range(pr.commits)):
        commit = all_commits[iter]
        for file in commit.files:
            if not check_file_include_rule(file.filename):
                continue
            filename, locale = handle_filename(file.filename, 2)
            if filename in pr_files_to_add or locale_check != locale:
                continue
            write_data(
                locale,
                filename,
                file.filename,
                commit_ref=commit.sha,
            )
            pr_files_to_add.append(filename)
            print(file)
    trans_db[locale_check].sync_pr_files(pr_files_to_add)


def load_pr_map() -> None:
    if not os.path.exists("trans_data/pr_map.json"):
        return
    with open("trans_data/pr_map.json", "r") as config, trans_db_lock:
        filestr = config.read()
        if not len(filestr):
            return
        parsed = json.loads(filestr)
        for lang, pr_str in parsed.items():
            if not trans_db.get(lang):
                trans_db[lang] = locale_t()
            with trans_db[lang].mutex:
                trans_db[lang].pr_no = pr_str
                get_by_pr(lang, int(pr_str))


def update_repo() -> None:
    def iter_contents(content, sectors: int) -> None:
        categorised: dict[str, dict[str, str]] = {}
        while content:
            file_content = content.pop(0)
            if file_content.type == "dir":
                content.extend(repo.get_contents(file_content.path))
            else:
                if not check_file_include_rule(file_content.path):
                    continue
                filename, locale = handle_filename(file_content.path, sectors)
                if not categorised.get(locale):
                    categorised[locale] = dict[str, str]()
                categorised[locale][filename] = file_content.path

        def process_locale(locale: str, files: dict[str, str]):
            ref = trans_db[locale]
            with ref.mutex:
                master_files_to_add: list[str] = []
                for filename, file_path in files.items():
                    if (
                        ref.pr_files
                        and filename in ref.pr_files
                    ):
                        continue
                    write_data(
                        locale,
                        filename,
                        file_path,
                    )
                    master_files_to_add.append(filename)
                ref.sync_master_files(master_files_to_add)

        process_locale(main_lang, categorised.pop(main_lang))

        for locale, files in categorised.items():
            process_locale(locale, files)

    # template_contents = repo.get_contents("public/templates")
    locale_contents = repo.get_contents("public/locales")
    with trans_db_lock if not trans_db_lock.locked() else nullcontext():
        for item in locale_contents:
            if item.type == "dir":
                locale_name = filename_rm_sector(item.path, 2)
                if not trans_db.get(locale_name):
                    trans_db[locale_name] = locale_t()
        # if not trans_db.get("templates"):
        #     trans_db["templates"] = locale_t()
    trans_db_lock.release()
    # iter_contents(template_contents, 1)
    iter_contents(locale_contents, 2)


def get_file_stat(lang: str) -> dict[str, bool]:
    def concat(entry: locale_t):
        return entry.owned_files + entry.pr_files

    def inner(base: list[str], target: list[str]) -> dict[str, bool]:
        ret = dict[str, bool]()
        for item in base:
            for nested_item in target:
                if item == nested_item:
                    ret[item] = True
                    break
            else:
                ret[item] = False
        return ret

    with trans_db[main_lang].mutex, trans_db[
        lang
    ].mutex if lang != main_lang else nullcontext():
        return inner(concat(trans_db[main_lang]), concat(trans_db[lang]))


def write_pr_map() -> None:
    out: dict[str, str] = {}
    with open("trans_data/pr_map.json", "w") as config:
        with trans_db_lock:
            for key, value in trans_db.items():
                with value.mutex:
                    if value.pr_no:
                        out[key] = value.pr_no
        config.write(json.dumps(out))


def initialize_github(token: str) -> None:
    global g, repo
    g = Github(token)
    repo = g.get_repo("placeTW/website")


def register_commands(tree, this_guild: discord.Object):
    with trans_db_lock:

        @tree.command(
            name="trans_stat",
            description="Get translation status",
            guild=this_guild,
        )
        @discord.app_commands.choices(
            lang=[Choice(name=lang, value=lang) for lang in trans_db.keys()]
        )
        async def trans_stat(
            interaction: discord.Interaction, lang: Choice[str]
        ):
            files_status = get_file_stat(lang.value)
            files_string = [
                f"{key}: {'Available' if value else 'Unavailable'}"
                for key, value in files_status.items()
            ]
            embed = discord.Embed(
                title="Translation Status",
                description="Comparing {} -> {}".format(lang.value, "en"),
            )
            embed.add_field(name="Files", value=files_string, inline=False)
            await interaction.response.send_message(embed=embed)
            return

        @tree.command(
            name="track_pr",
            description="Make language track translation pull request",
            guild=this_guild,
        )
        @discord.app_commands.choices(
            lang=[Choice(name=lang, value=lang) for lang in trans_db.keys()]
        )
        @app_commands.describe(pr_no="The string you want echoed backed")
        async def track_pr(
            interaction: discord.Interaction, lang: Choice[str], pr_no: int
        ):
            with trans_db[lang.value].mutex:
                loading_msg = interaction.response.send_message(
                    "Performing action..."
                )
                get_by_pr(lang.value, pr_no)
                ref = trans_db[lang.value]
                ref.pr_no = pr_no
                embed = discord.Embed(
                    title=f"Translation for {lang.value}",
                    description=f"{lang.value} is now tracking PR {ref.pr_no}",
                )
                pr_files: str = "".join([f"{file}\n" for file in ref.pr_files])
                master_files: str = "".join(
                    [f"{file}" for file in ref.owned_files]
                )
                embed.add_field(
                    name="Files from pull request",
                    value=pr_files if len(pr_files) else "None",
                    inline=False,
                )
                embed.add_field(
                    name="Files from master",
                    value=master_files if len(master_files) else "None",
                    inline=False,
                )
                await loading_msg
                await interaction.edit_original_response(
                    content=None, embed=embed
                )
