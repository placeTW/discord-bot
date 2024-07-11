from enum import StrEnum
import json
from pathlib import Path
from pydantic import BaseModel
from re import compile, IGNORECASE, UNICODE
from discord import Message

from modules.probability import mock_bernoulli

class ReactReplyType(StrEnum):
    text = "text"
    image = "image"
    video = "video"
    audio = "audio"
    file = "file"

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
    type: ReactReplyType = "text"

class ReactResource(BaseModel):
    matches: list[ReactMatches]
    possible_reactions: list[ReactPossibleReaction]
    replies: list[ReactReply]
    

REACT_RESOURCES_DIR = Path(Path(__file__).parent, "..", "resources", "reacts")


def load_react_resources() -> dict[str, ReactResource]:
    resources = {}
    for file in REACT_RESOURCES_DIR.iterdir():
        with open(file, "r") as f:
            filename = file.stem
            data = json.load(f)
            resources[filename] = ReactResource(**data)
    return resources


REACT_RESOURCES: dict[str, ReactResource] = load_react_resources()

def check_matches(message_content: str, matches: list[ReactMatches]) -> bool:
    for possible_match in matches:
        if possible_match.match_whole_word:
            if compile(rf"\b(?:{'|'.join(possible_match.keywords)})\b", IGNORECASE | UNICODE).search(message_content):
                return True
        else:
            if compile(rf"{'|'.join(possible_match.keywords)}", IGNORECASE | UNICODE).search(message_content):
                return True
    return False


async def handle_react(message: Message)  -> list[str]:
    events = []
    for event_name, resource in REACT_RESOURCES.items():
        if check_matches(message.content, resource.matches):
            for possible_reaction in resource.possible_reactions:
                for reaction in possible_reaction.reactions:
                    if possible_reaction.react_with_all:
                        await message.add_reaction(reaction)
                    else:
                        if mock_bernoulli(possible_reaction.chance):
                            await message.add_reaction(reaction)
            for reply in resource.replies:
                if mock_bernoulli(reply.chance):
                    # TODO: Handle different types of replies
                    await message.reply(reply.message)
            events.append(event_name)
            
    return events