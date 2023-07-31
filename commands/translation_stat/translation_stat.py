from github import Github
import json
import os
from multiprocessing import Process
from filelock import FileLock

g = Github()
repo = g.get_repo("placeTW/website")
tracking_files = ["translation.json", "art-pieces.json"]

def filename_rm_sector(filename: str, sectors: int) -> str:
    index = 0
    for i in range(sectors):
        index = filename.find('/', index + 1)
        if index == -1:
            raise IndexError("Not enough sectors for string {}".format(filename))
    return filename[index + 1:];

def handle_filename(filename: str, sectors: int) -> tuple[str, str]:
    filename = filename_rm_sector(filename, sectors)
    locale = filename[:filename.find('/')]
    filename = filename_rm_sector(filename, 1)
    return filename, locale

def write_data(locale: str, filename: str, full_path: str, commit_ref: str = None, success_callback = None) -> None:
    if not filename in tracking_files:
        return
    if not os.path.exists("trans_data/{}".format(locale)):
        os.makedirs("trans_data/{}".format(locale))
    with open("trans_data/{}/{}".format(locale, filename), "w+") as out:
        if not commit_ref:
            out.write(repo.get_contents(full_path).decoded_content.decode("utf-8"))
        else:
            out.write(repo.get_contents(full_path, ref = commit_ref).decoded_content.decode("utf-8"))
    if success_callback:
        success_callback()

class locale_t:
    def __init__(self) -> None:
        self.owned_files: list[str] = []
        self.pr_files: list[str] = []
        self.pr_no: str = None
    def add_file(self, filename) -> None:
        if not filename in self.owned_files:
            self.owned_files.append(filename)
    def add_pr_file(self, filename) -> None:
        if not self.pr_files:
            self.pr_files = list[str]()
        if filename in self.owned_files:
            self.owned_files.remove(filename)
        self.pr_files.append(filename)
    def __repr__(self) -> str:
        return "Owned files: {}\nPR files: {}\nPR number: {}\n".format(self.owned_files, self.pr_files, self.pr_no)
    def toJSON(self):
        return "{ \"pr_no\": \"{}\" }".format(self.pr_no)

trans_db: dict[str, locale_t] = {}

def get_by_pr (locale_check: str, pr_no: int)-> None:
    pr = repo.get_pull(pr_no);
    commit = pr.get_commits()[pr.commits - 1]
    for file in commit.files:
        filename, locale = handle_filename(file.filename, 2)
        if locale_check != locale:
            continue
        write_data (locale, filename, file.filename, commit_ref = commit.sha, success_callback = lambda: trans_db[locale].add_pr_file(file.filename))

def load_pr_map () -> None:
    if not os.path.exists("trans_data/pr_map.json"):
        return
    with open("trans_data/pr_map.json", "r") as config:
        parsed = json.loads(config.read())
        for key, item in parsed:
            trans_db[key].pr_no = str(item["pr_no"])
            get_by_pr(key, int(item["pr_no"]))

def init_repo () -> None:
    def iter_contents (content, sectors: int) -> None:
        while content:
            file_content = content.pop(0)
            if file_content.type == "dir":
                content.extend(repo.get_contents(file_content.path))
            else:
                filename, locale = handle_filename(file_content.path, sectors)
                if trans_db[locale].pr_files and file_content.path in trans_db[locale].pr_files:
                    return
                write_data(locale, filename, file_content.path, success_callback = lambda: trans_db[locale].add_file(filename))

    template_contents = repo.get_contents("public/templates")
    locale_contents = repo.get_contents("public/locales")
    for item in locale_contents:
        if item.type == "dir":
            trans_db[filename_rm_sector(item.path, 2)] = locale_t()
    trans_db["templates"] = locale_t()
    load_pr_map()
    iter_contents(template_contents, 1)
    iter_contents(locale_contents, 2)

def write_trans_db() -> None:
    config = open("trans_data/trans_db.json", "w")
    json.dump(trans_db, config)
    config.close()

init_repo()
print(trans_db)
