from github import Github, Repository
import json
import os
import time
from threading import Lock
from discord.ext import tasks, commands
import discord
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
        return "Owned files: {}\nPR files: {}\nPR number: {}\n".format(
            self.owned_files, self.pr_files, self.pr_no
        )

    def toJSON(self):
        return '{ "pr_no": "{}" }'.format(self.pr_no)


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
                file.filename
            ),
        )


def load_pr_map() -> None:
    if not os.path.exists("trans_data/pr_map.json"):
        return
    with open("trans_data/pr_map.json", "r") as config:
        parsed = json.loads(config.read())
        for key, item in parsed:
            with trans_db[key].mutex:
                trans_db[key].pr_no = str(item["pr_no"])
                get_by_pr(key, int(item["pr_no"]))


def update_repo() -> None:
    print("UPDATE REPO INVOKED")

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
    load_pr_map()
    # iter_contents(template_contents, 1)
    iter_contents(locale_contents, 2)


def get_file_stat(lang: str) -> dict[str, bool]:
    concat = lambda entry: entry.owned_files + entry.pr_files

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

        with trans_db["eng"].mutex, trans_db[
            lang
        ].mutex if lang != "eng" else nullcontext():
            return inner(concat(trans_db["eng"]), concat(trans_db[str]))


def write_trans_db() -> None:
    with open("trans_data/trans_db.json", "w") as config:
        json.dump(trans_db, config)
        config.close()


def initialize_github(token: str) -> None:
    global g, repo
    g = Github(token)
    repo = g.get_repo("placeTW/website")


class bg_worker(commands.Cog):
    def __init__(self, github_token: str):
        initialize_github(github_token)
        self.task.start()

    @tasks.loop(hours=1)
    async def task(self) -> None:
        update_repo()


def register_commands(tree, this_guild: discord.Object):
    print("READY")
    with trans_db_lock:
        for lang in trans_db.keys():
            print(lang)
        return
        @tree.command(
            name="trans_stat",
            description="Get translation status",
            guild=this_guild,
        )
        @discord.app_commands.choices(
            lang=[
                Choice(name=lang, value=lang) for lang in trans_db.keys()
            ]
        )
        async def trans_stat(interaction: discord.Interaction, lang: Choice[str]):
            files_status = get_file_stat(lang.value)
            files_string = ""
            for key, value in files_status:
                files_string.join(
                    "{}: {}\n".format(key, value and "Available" or "Unavailable")
                )
            embed = discord.Embed(
                title="Translation Status",
                description="Comparing {} -> {}".format(lang.value, "eng"),
            )
            embed.add_field(name="Files", value=files_string, inline=False)
            await interaction.response.send_message(embed=embed)
            return
