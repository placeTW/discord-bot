from github import Github, Repository, GithubObject
import json
import os
from threading import Lock, Condition
from contextlib import nullcontext
import re

g: Github = None
repo: Repository = None

# repo = g.get_repo("placeTW/website")
main_lang = "en"
json_matches: dict[str, list[str]] = {
    "art-pieces.json": [r".*#(title|blurb|desc)"],
    "translation.json": [r".*"],
}

commands_initialize_condition = Condition()
commands_initialize_condition_flag = False

def check_file_include_rule(path: str) -> bool:
    return re.search(
        r"public\/locales\/.*\/(art-pieces\.json|translation\.json)", path
    )


def filename_rm_sector(filename: str, sectors: int) -> str:
    index = 0
    for i in range(sectors):
        index = filename.find("/", index + 1)
        if index == -1:
            raise IndexError(
                "Not enough sectors for string {}".format(filename)
            )
    return filename[index + 1 :]


def handle_filename(filename: str, sectors: int) -> tuple[str, str]:
    filename = filename_rm_sector(filename, sectors)
    locale = filename[: filename.find("/")]
    filename = filename_rm_sector(filename, 1)
    return filename, locale


def generate_progress_str(percentage: float, size: int) -> str:
    slice = 1 / size
    return "[{}]".format(str().join([
        f"{'⬜' if slice * (it + 1) < percentage else '⬛'}"
        for it in range(size)
    ]))


class transfile_progress:
    def __init__(self):
        # self.all_fields: dict[str, bool] = {}
        self.all_fields: dict = {}
        self.ready_indexes = int()
        self.total_indexes = int()

    def progress_str_fwd(self) -> str:
        return generate_progress_str(
            self.ready_indexes / self.total_indexes, 10
        )

    def load_file(
        self, filename, json_data: dict, lang_cmp: "transfile_progress" = None
    ) -> None:
        standards: list[list[str]] = []
        tmp_store: dict[str, str] = {}

        for item in json_matches[filename]:
            standards.append(item.split("#"))

        def match(target: dict, iter=0, pre_str=[""]) -> None:
            nonlocal standards
            for key, value in target.items():
                for item in standards:
                    if re.match(item[iter], key):
                        pre_str[0] += f"{'/' if iter != 0 else ''}{key}"
                        if iter + 1 == len(item):
                            tmp_store[pre_str[0]] = str(value)
                        else:
                            match(value, iter + 1, pre_str)
                        prev_slash = pre_str[0].rfind("/")
                        pre_str[0] = pre_str[0][: prev_slash if prev_slash != -1 else 0]
                        break

        match(json_data)
        if not lang_cmp:
            self.all_fields = tmp_store
            self.ready_indexes = self.total_indexes = len(
                self.all_fields.keys()
            )
        else:
            for key, value in lang_cmp.all_fields.items():
                obj = tmp_store.get(key)
                self.all_fields[key] = not (not obj or obj == value)
            self.total_indexes = len(self.all_fields.keys())
            self.ready_indexes = sum(self.all_fields.values())

    def write_json(self, locale, filename) -> None:
        out: dict = {}
        out["total_indexes"] = self.total_indexes
        out["ready_indexes"] = self.ready_indexes
        if locale != main_lang:
            out["all_fields"] = self.all_fields
        else:
            out["all_fields"] = dict(zip(self.all_fields.keys(), [True for _ in range(len(self.all_fields.keys()))]))
        with open(f"trans_data/{locale}/{filename}_progress.json", "w+") as target:
            target.write(json.dumps(out))

    def read_json(self, locale, filename) -> None:
        with open(f"trans_data/{locale}/{filename}_progress.json", "r") as target:
            parsed = json.loads(target.read())
            self.total_indexes = parsed["total_indexes"]
            self.ready_indexes = parsed["ready_indexes"]
            self.all_fields = parsed["all_fields"]


def get_transfile_progress(locale, filename, lock: bool) -> transfile_progress:
    with trans_db[locale].mutex if lock else nullcontext():
        ret = transfile_progress()
        ret.read_json(locale, filename)
        return ret


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

    def all_files(self):
        return self.owned_files + self.pr_files


trans_db_lock = Lock()
trans_db: dict[str, locale_t] = {}


def shift2pr(locale_check: str, pr_no: int) -> None:
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
    trans_db[locale_check].sync_pr_files(pr_files_to_add)


def apply_pr_map() -> None:
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
                shift2pr(lang, int(pr_str))



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

    main_lang_progress: dict[str, transfile_progress] = {}

    def process_locale(locale: str, files: dict[str, str]):
        nonlocal main_lang_progress
        ref = trans_db[locale]
        with ref.mutex:
            master_files_to_add: list[str] = []
            for filename, file_path in files.items():
                if not (ref.pr_files and filename in ref.pr_files):
                    write_data(
                        locale,
                        filename,
                        file_path,
                    )
                    master_files_to_add.append(filename)
                with open(f"trans_data/{locale}/{filename}", "r") as target_file:
                    if locale == main_lang:
                        main_lang_progress[filename] = transfile_progress()
                        main_lang_progress[filename].load_file(filename, json.loads(target_file.read()))
                        main_lang_progress[filename].write_json(locale, filename)
                    else:
                        other_lang_progress = transfile_progress()
                        other_lang_progress.load_file(filename, json.loads(target_file.read()), main_lang_progress[filename])
                        other_lang_progress.write_json(locale, filename)
           
            ref.sync_master_files(master_files_to_add)

    if categorised.get(main_lang):
        process_locale(main_lang, categorised.pop(main_lang))
    else:
        ref = trans_db[main_lang]
        with ref.mutex:
            for file in ref.all_files():
                main_lang_progress[file] = transfile_progress()
                main_lang_progress[file].read_json(main_lang, file)

    for locale, files in categorised.items():
        process_locale(locale, files)


def update_repo() -> None:
    # template_contents = repo.get_contents("public/templates")
    locale_contents = repo.get_contents("public/locales")
    with trans_db_lock:
        for item in locale_contents:
            if item.type == "dir":
                locale_name = filename_rm_sector(item.path, 2)
                if not trans_db.get(locale_name):
                    trans_db[locale_name] = locale_t()
        # if not trans_db.get("templates"):
        #     trans_db["templates"] = locale_t()
    with commands_initialize_condition:
        commands_initialize_condition.notify()
        global commands_initialize_condition_flag
        commands_initialize_condition_flag = True
    # iter_contents(template_contents, 1)
    iter_contents(locale_contents, 2)


# FIXME This is likely to cause race condition idk how to prevent it
def shift2master(locale: str) -> None:
    trans_db[locale].pr_files = None
    iter_contents(repo.get_contents(f"public/locales/{locale}", 2))


def get_file_stat(lang: str) -> dict[str, bool]:

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
        return inner(trans_db[main_lang].all_files(), trans_db[lang].all_files())


def write_pr_map() -> None:
    out: dict[str, str] = {}
    with open("trans_data/pr_map.json", "w+") as config:
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
