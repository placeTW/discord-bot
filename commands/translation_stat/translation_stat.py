from github import Github, Repository
import json
import os
from threading import Lock
import discord
from discord import app_commands
from discord.app_commands import Choice
from contextlib import nullcontext

g: Github = None
repo: Repository = None

# repo = g.get_repo("placeTW/website")
tracking_files = ["translation.json", "art-pieces.json"]


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


def write_data(
    locale: str,
    filename: str,
    full_path: str,
    commit_ref: str = None,
    success_callback=None,
) -> None:
    if filename not in tracking_files:
        return
    if not os.path.exists("trans_data/{}".format(locale)):
        os.makedirs("trans_data/{}".format(locale))
    with open("trans_data/{}/{}".format(locale, filename), "w+") as out:
        if not commit_ref:
            out.write(
                repo.get_contents(full_path).decoded_content.decode("utf-8")
            )
        else:
            out.write(
                repo.get_contents(
                    full_path, ref=commit_ref
                ).decoded_content.decode("utf-8")
            )
    if success_callback:
        success_callback()


class locale_t:
    def __init__(self) -> None:
        self.owned_files: list[str] = None
        self.pr_files: list[str] = []
        self.pr_no: str = None
        self.mutex: Lock = Lock()

    def add_file(self, filename) -> None:
        if not self.owned_files:
            self.owned_files = list[str]()
        if filename not in self.owned_files:
            self.owned_files.append(filename)

    def add_pr_file(self, filename) -> None:
        if not self.pr_files:
            self.pr_files = list[str]()
        if filename in self.owned_files:
            self.owned_files.remove(filename)
        self.pr_files.append(filename)

    def __repr__(self) -> str:
        return f"Owned files: {self.owned_files}\nPR files: {self.pr_files}\nPR number: {self.pr_no}\n"



trans_db_lock = Lock()
trans_db: dict[str, locale_t] = {}


def get_by_pr(locale_check: str, pr_no: int) -> None:
    pr = repo.get_pull(pr_no)
    commit = pr.get_commits()[pr.commits - 1]
    for file in commit.files:
        filename, locale = handle_filename(file.filename, 2)
        if locale_check != locale:
            continue
        write_data(
            locale,
            filename,
            file.filename,
            commit_ref=commit.sha,
            success_callback=lambda: trans_db[locale].add_pr_file(
                filename
            ),
        )


def load_pr_map() -> None:
    if not os.path.exists("trans_data/pr_map.json"):
        return
    with open("trans_data/pr_map.json", "r") as config, trans_db_lock:
        filestr = config.read()
        if not len(filestr):
            return
        parsed = json.loads(filestr)
        for key, item in parsed:
            if not trans_db.get(key):
                trans_db[key] = locale_t()
            with trans_db[key].mutex:
                trans_db[key].pr_no = str(item["pr_no"])
                get_by_pr(key, int(item["pr_no"]))


def update_repo() -> None:
    def iter_contents(content, sectors: int) -> None:
        while content:
            file_content = content.pop(0)
            if file_content.type == "dir":
                content.extend(repo.get_contents(file_content.path))
            else:
                filename, locale = handle_filename(file_content.path, sectors)
                with trans_db[locale].mutex:
                    if (
                        trans_db[locale].pr_files
                        and file_content.path in trans_db[locale].pr_files
                    ):
                        return
                    write_data(
                        locale,
                        filename,
                        file_content.path,
                        success_callback=lambda: trans_db[locale].add_file(
                            filename
                        ),
                    )

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
    def concat(entry: locale_t): return entry.owned_files + entry.pr_files

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

    with trans_db["en"].mutex, trans_db[
        lang
    ].mutex if lang != "en" else nullcontext():
        return inner(concat(trans_db["en"]), concat(trans_db[lang]))


def write_pr_map() -> None:
    out: dict[str, str] = {}
    with open("trans_data/pr_map.json", "w") as config:
        with trans_db_lock:
            for key, value in trans_db.items():
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
        async def trans_stat(interaction: discord.Interaction, lang: Choice[str]):
            files_status = get_file_stat(lang.value)
            files_string = [f"{key}: {'Available' if value else 'Unavailable'}" for key, value in files_status.items()]
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
            guild=this_guild
        )
        @discord.app_commands.choices(
            lang=[Choice(name=lang, value=lang) for lang in trans_db.keys()]
        )
        @app_commands.describe(pr_no="The string you want echoed backed")
        async def track_pr(interaction: discord.Interaction, lang: Choice[str], pr_no: int):
            with trans_db[lang.value].mutex:
                loading_msg = interaction.response.send_message("Performing action...")
                get_by_pr(lang.value, pr_no)
                ref = trans_db[lang.value]
                ref.pr_no = pr_no
                embed = discord.Embed(
                    title=f"Translation for {lang.value}",
                    description=f"{lang.value} is now tracking PR {ref.pr_no}"
                )
                pr_files: str = "".join([f"{file}\n" for file in ref.pr_files])
                master_files: str = "".join([f"{file}" for file in ref.owned_files])
                embed.add_field(name="Files from pull request", value=pr_files if len(pr_files) else "None", inline=False)
                embed.add_field(name="Files from master", value=master_files if len(master_files) else "None", inline=False)
                await loading_msg
                await interaction.edit_original_response(content=None, embed=embed)
