import json
from pathlib import Path
from pydantic import BaseModel

class ReactMatches(BaseModel):
    match_whole_word: bool
    keywords: list[str]


class ReactPossibleReaction(BaseModel):
    chance: float
    reactions: list[str]
    react_with_all: bool = False


class ReactReply(BaseModel):
    chance: float
    message: str
    type: str = "text"


class ReactResource(BaseModel):
    matches: list[ReactMatches]
    possible_reactions: list[ReactPossibleReaction]
    replies: list[ReactReply]
    


REACT_RESOURCES_DIR = Path(Path(__file__).parent, "..", "resources", "reacts")


def load_react_resources():
    resources = []
    for file in REACT_RESOURCES_DIR.iterdir():
        with open(file, "r") as f:
            data = json.load(f)
            resources.append(ReactResource(**data))
    return resources


print(load_react_resources())
