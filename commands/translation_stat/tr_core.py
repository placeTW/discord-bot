from github import Github, Repository, GithubObject
import json
import os
from threading import Lock, Event
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

commands_initialize_condition = Event()

lang_require_update: bool = False

def float_to_percentage(target: float) -> int:
    return int(target * 100 + 1)

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


def generate_progress_str(percentage: int, size: int) -> str:
    slice = (100 / size) + 1
    return "[{}]".format(
        str().join(
            [
                f"{'⬜' if slice * (it + 1) < percentage else '⬛'}"
                for it in range(size)
            ]
        )
    )


class transfile_progress:
    def __init__(self):
        # self.all_fields: dict[str, bool] = {}
        self.all_fields: dict = {}
        self.ready_indexes = int()
        self.total_indexes = int()

    def progress_str_fwd(self) -> str:
        return generate_progress_str(
            float_to_percentage(self.ready_indexes / self.total_indexes), 10
        )

    def get_percentage(self) -> int:
        return float_to_percentage(self.ready_indexes / self.total_indexes)

    def to_progress_str(self) -> str:
        return f"{self.ready_indexes}/{self.total_indexes}, {self.get_percentage()}%"

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
                        pre_str[0] = pre_str[0][
                            : prev_slash if prev_slash != -1 else 0
                        ]
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
            out["all_fields"] = dict(
                zip(
                    self.all_fields.keys(),
                    [True for _ in range(len(self.all_fields.keys()))],
                )
            )
        with open(
            os.path.join("trans_data", locale, f"{filename}_progress.json"), "w+"
        ) as target:
            target.write(json.dumps(out))

    def read_json(self, locale, filename) -> None:
        with open(
            os.path.join("trans_data", locale, f"{filename}_progress.json"), "r"
        ) as target:
            parsed = json.loads(target.read())
            self.total_indexes = parsed["total_indexes"]
            self.ready_indexes = parsed["ready_indexes"]
            self.all_fields = parsed["all_fields"]


def read_transfile_progress(locale, filename) -> transfile_progress:
    ret = transfile_progress()
    ret.read_json(locale, filename)
    return ret


def write_data(
    locale: str,
    filename: str,
    full_path: str,
    commit_ref: str = GithubObject.NotSet,
) -> None:
    if not os.path.exists(os.path.join("trans_data", locale)):
        os.makedirs(os.path.join("trans_data", locale).format(locale))
    with open(os.path.join("trans_data", locale, filename), "w+") as out:
        out.write(
            repo.get_contents(
                full_path, ref=commit_ref
            ).decoded_content.decode("utf-8")
        )


class locale_t:
    def __init__(self) -> None:
        self.owned_files: list[str] = []
        self.pr_files: list[str] = []
        self.pr_no: int = None
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


# Lock b4 call this
def shift2pr(locale_check: str, pr_no: int) -> None:
    trans_db[locale_check].pr_no = pr_no
    main_lang_progress = gen_mainlang_progress_map(locale_check != "en")
    iter_pr(repo.get_pull(pr_no), locale_check, main_lang_progress)
    print(f"{locale_check} => PR {pr_no}")


def iter_pr(pr, locale_check: str, main_lang_progress=None):
    print(f"{locale_check} iter PR {pr.number}")
    pr_files_to_add: list[str] = []
    all_commit = pr.get_commits()
    for iter in reversed(range(pr.commits)):
        commit = all_commit[iter]
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
                commit_ref=commit.sha
            )
            pr_files_to_add.append(filename)
    trans_db[locale_check].sync_pr_files(pr_files_to_add)
    for file in pr_files_to_add:
        write_progress_proxy(locale_check, filename, main_lang_progress)


def apply_pr_map() -> None:
    if not os.path.exists(os.path.join("trans_data", "pr_map.json")):
        return
    with open(os.path.join("trans_data", "pr_map.json"), "r") as config, trans_db_lock:
        filestr = config.read()
        if not len(filestr):
            return
        parsed = json.loads(filestr)
        for lang, pr_no in parsed.items():
            if not trans_db.get(lang):
                trans_db[lang] = locale_t()
            with trans_db[lang].mutex:
                trans_db[lang].pr_no = pr_no
            print(f"{lang} => PR {pr_no}")
    global lang_require_update
    lang_require_update = True


def gen_mainlang_progress_map(
    lock: bool,
) -> dict[str, transfile_progress]:
    with trans_db["en"].mutex if lock else nullcontext():
        target_files: list[str] = []
        for _, _, subfiles in os.walk(os.path.join("trans_data", "en")):
            for item in subfiles:
                if not item.endswith("_progress.json"):
                    target_files.append(item)
        ret: dict[str, transfile_progress] = {}
        for item in target_files:
            progress = transfile_progress()
            progress.read_json("en", item)
            ret[item] = progress
        return ret


def write_transfile_progress(
    locale: str, filename: str, main_lang_progress: transfile_progress = None
) -> transfile_progress:
    target = transfile_progress()
    with open(os.path.join("trans_data", locale, filename), "r") as target_file:
        if locale == main_lang_progress:
            target.load_file(filename, json.loads(target_file.read()))
        else:
            target.load_file(
                filename, json.loads(target_file.read()), main_lang_progress
            )
    target.write_json(locale, filename)
    return target


def write_progress_proxy(locale: str, filename: str, main_lang_progress: dict[str, transfile_progress] = None) -> None:
    if locale == main_lang:
        res = write_transfile_progress(locale, filename)
        if main_lang_progress is not None:
            main_lang_progress[filename] = res
    else:
        if main_lang_progress is None:
            main_lang_progress = gen_mainlang_progress_map(True)
        write_transfile_progress(
            locale, filename, main_lang_progress[filename]
        )


def iter_master(locale_check: str, content, main_lang_progress=None, sectors: int = 2) -> None:
    print(f"{locale_check} iter master")
    ref = trans_db[locale_check]
    files_to_add: list[str] = []
    while content:
        file_content = content.pop(0)
        if file_content.type == "dir":
            content.extend(repo.get_contents(file_content.path))
        else:
            if not check_file_include_rule(file_content.path):
                continue
            filename, locale = handle_filename(file_content.path, sectors)
            if locale_check != locale or (ref.pr_no and filename in ref.pr_files):
                continue
            write_data(locale, filename, file_content.path)
            files_to_add.append(filename)

    ref.sync_master_files(files_to_add)

    for file in files_to_add:
        write_progress_proxy(locale, file, main_lang_progress)


def update_locale(locale: str, main_lang_progress: transfile_progress = None):
    ref = trans_db[locale]
    with ref.mutex:
        if ref.pr_no:
            iter_pr(repo.get_pull(ref.pr_no), locale, main_lang_progress)
        try:
            iter_master(locale, repo.get_contents(f"public/locales/{locale}"), main_lang_progress)
        except Exception:
            if not ref.pr_no:
                raise


def update_repo() -> None:
    locale_contents = repo.get_contents("public/locales")
    lang_list: list[str] = []
    with trans_db_lock:
        for item in locale_contents:
            if item.type == "dir":
                locale_name = filename_rm_sector(item.path, 2)
                if not trans_db.get(locale_name):
                    trans_db[locale_name] = locale_t()
                    global lang_require_update
                    lang_require_update = True
        lang_list = list(trans_db.keys())
    if not commands_initialize_condition.is_set():
        commands_initialize_condition.set()
    main_lang_progress: dict[str, transfile_progress] = {}
    update_locale(lang_list.pop(lang_list.index("en")), main_lang_progress)
    for item in lang_list:
        update_locale(item, main_lang_progress)


def shift2master(locale: str) -> None:
    trans_db[locale].pr_no = None
    trans_db[locale].pr_files.clear()
    main_lang_progress = gen_mainlang_progress_map(locale != main_lang)
    iter_master(locale, repo.get_contents(f"public/locales/{locale}"), main_lang_progress)
    print(f"{locale} => master")


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
        return inner(
            trans_db[main_lang].all_files(), trans_db[lang].all_files()
        )


def write_pr_map() -> None:
    out: dict[str, str] = {}
    with open(os.path.join("trans_data", "pr_map.json"), "w+") as config:
        with trans_db_lock:
            for key, value in trans_db.items():
                with value.mutex:
                    if value.pr_no:
                        out[key] = value.pr_no
        config.write(json.dumps(out))


def initialize_github(token: str) -> None:
    global g, repo
    if not token:
        g = Github()
    else:
        g = Github(token)
    
    repo = g.get_repo("placeTW/website")
