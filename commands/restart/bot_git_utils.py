
from os import getenv
from dotenv import load_dotenv
from github import Auth, Github

load_dotenv()


GITHUB_TOKEN = getenv("GITHUB_TOKEN")
# using an access token
GITHUB_AUTH = Auth.Token(GITHUB_TOKEN)
# Enter public web Github
GITHUB_OBJECT = Github(auth=GITHUB_AUTH)
REPO_NAME = 'placeTW/discord-bot'
BOT_REPO = GITHUB_OBJECT.get_repo(REPO_NAME)

def list_of_branches():
    return ['main'] + [branch.name for branch in BOT_REPO.get_branches() if branch.name != 'main']