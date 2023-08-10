from github.Repository import Repository
from github.ContentFile import ContentFile
from github.GithubException import UnknownObjectException
from github import Github
from os import getenv
from github import Auth
import json
from dotenv import load_dotenv
from pathlib import Path
from ..entry_consts.consts import SUPPORTED_LANGUAGE_CODES

DOTENV_FILEPATH = (Path(__file__) / "../../../.env").resolve()

load_dotenv(DOTENV_FILEPATH)
GITHUB_TOKEN = getenv("GITHUB_TOKEN")
# using an access token
GITHUB_AUTH = Auth.Token(GITHUB_TOKEN)
# Enter public web Github
GITHUB_OBJECT = Github(auth=GITHUB_AUTH)
# get the specific repo
REPO_NAME = "placeTW/website"
WEBSITE_REPO = GITHUB_OBJECT.get_repo(REPO_NAME)

BRANCH_NAME = "bot-i18n-commits"


def determine_file_path_on_repo(lang: str):
    if lang not in SUPPORTED_LANGUAGE_CODES:
        print(f"Language {lang} not supported!")
        return None
    return f"public/locales/{lang}/art-pieces.json"


def get_json_file_from_repo(file_path: str, branch_name: str = BRANCH_NAME):
    global WEBSITE_REPO
    try:
        return WEBSITE_REPO.get_contents(file_path, ref=branch_name)
    except UnknownObjectException:
        return None


def create_pull_request(
    lang: str, new_json_contents: dict, entry_id: str, field: str
):
    # ! new_json_contents is the ENTIRE json, not just one entry or field
    global GITHUB_OBJECT, BRANCH_NAME
    file_path = determine_file_path_on_repo(lang)
    if file_path is None:  # unsupported language
        return None
    # * From this point, the dir must exist, so the only
    # *   exception is that the art-pieces file doesn't.

    # ! Convert JSON to string.
    new_json_contents_str = json.dumps(
        new_json_contents, indent=2, ensure_ascii=False
    )
    # * The idea is: if file exists, replace it with new version.
    # * The idea is: if file doesn't exist, create it and place new json.
    try:
        json_file = get_json_file_from_repo(file_path, BRANCH_NAME)
        update_and_commit_file(
            json_file,
            commit_msg=f"Modified translation for: lang={lang}, entry_id={entry_id}, field={field}",
            new_contents=new_json_contents_str,
        )
    except (UnknownObjectException, AttributeError):
        # file doesn't exist, create and commit a new one
        # ! Note that this immediately commits the new file!
        json_file = WEBSITE_REPO.create_file(
            file_path,
            message=f"Create art-pieces file for {lang}",
            content=new_json_contents_str,  # Create empty file
            branch=BRANCH_NAME,
        )


def update_and_commit_file(
    file: ContentFile,
    commit_msg: str,
    new_contents: str,
    branch_name: str = BRANCH_NAME,
):
    WEBSITE_REPO.update_file(
        path=file.path,
        message=commit_msg,
        content=new_contents,
        sha=file.sha,
        branch=branch_name,
    )


if __name__ == "__main__":
    create_pull_request("fr")
