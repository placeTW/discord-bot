from enum import StrEnum
import json
from pathlib import Path
from pydantic import BaseModel
from re import compile, IGNORECASE, UNICODE
from discord import Message
from random import choice, sample

from modules.probability import mock_bernoulli

class ReactReplyType(StrEnum):
    text = "text"
    image = "image"
    video = "video"
    audio = "audio"
    file = "file"

class ReactMatches(BaseModel):
    id: str = ""
    match_whole_word: bool
    keywords: list[str]

class ReactPossibleReaction(BaseModel):
    id: str = ""
    chance: float
    reactions: list[str]
    react_with_all: bool = False
    react_only_one: bool = False

class ReactReply(BaseModel):
    chance: float
    message: str
    type: ReactReplyType = "text"

class ReactResource(BaseModel):
    matches: list[ReactMatches]
    possible_reactions: list[ReactPossibleReaction] | None = None
    replies: list[ReactReply] | None = None
    

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

# For testing
def check_resource_match(message_content: str, resource_name: str) -> bool:
    resource = REACT_RESOURCES[resource_name]
    return check_matches(message_content, resource.matches)

def check_matches(message_content: str, matches: list[ReactMatches]) -> bool:
    for possible_match in matches:
        if possible_match.match_whole_word:
            if compile(rf"\b(?:{'|'.join(possible_match.keywords)})\b", flags=IGNORECASE | UNICODE).search(message_content):
                return True
        else:
            if compile(rf"{'|'.join(possible_match.keywords)}", flags=IGNORECASE | UNICODE).search(message_content):
                return True
    return False

async def react_to_message(message: Message, possible_reactions: list[ReactPossibleReaction]) -> None:
    for possible_reaction in sample(possible_reactions, len(possible_reactions)): # Shuffle the reactions
        if possible_reaction.react_only_one: # If only one of the possible reactions should be added
            await message.add_reaction(choice(possible_reaction.reactions))
        else:
            for reaction in possible_reaction.reactions: # If all of the possible reactions should be added
                if possible_reaction.react_with_all:
                    await message.add_reaction(reaction)
                else: # If the reaction should be added with a certain chance
                    if mock_bernoulli(possible_reaction.chance):
                        await message.add_reaction(reaction)

async def reply_to_message(message: Message, replies: list[ReactReply]) -> None:
    for reply in replies:
        if mock_bernoulli(reply.chance):
            # TODO: Handle different types of replies
            await message.reply(reply.message)


async def handle_message_react(message: Message)  -> list[str]:
    events = []
    for event_name, resource in REACT_RESOURCES.items():
        if check_matches(message.content, resource.matches):
            if resource.possible_reactions:
                await react_to_message(message, resource.possible_reactions)
            if resource.replies:
                await reply_to_message(message, resource.replies)
            events.append(event_name)
            
    return events