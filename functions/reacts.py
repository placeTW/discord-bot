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
    match_whole_word: bool
    keywords: list[str]
    match_link_id: str = ""

class ReactPossibleReaction(BaseModel):
    chance: float
    reactions: list[str]
    match_link_id: str = ""
    other_match_link_ids: list[str] = []
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
    matches = check_matches(message_content, resource.matches)
    return bool(matches)

def check_matches(message_content: str, matches: list[ReactMatches]) -> bool | set[str]:
    match_id_results = set()
    found_match = False
    for possible_match in matches:
        if possible_match.match_whole_word:
            if compile(rf"\b(?:{'|'.join(possible_match.keywords)})\b", flags=IGNORECASE | UNICODE).search(message_content):
                found_match = True
                if possible_match.match_link_id:
                    match_id_results.add(possible_match.match_link_id)
        else:
            if compile(rf"{'|'.join(possible_match.keywords)}", flags=IGNORECASE | UNICODE).search(message_content):
                found_match = True
                if possible_match.match_link_id:
                    match_id_results.add(possible_match.match_link_id)
    # Return the link IDs if there are any, otherwise return if there was a match
    return match_id_results if len(match_id_results) > 0 else found_match

async def react_to_message(message: Message, possible_reactions: list[ReactPossibleReaction], match_id_results: set[str] = None) -> None:
    for possible_reaction in possible_reactions:
        # If the matched linked results exists, check if the reaction is linked to any of the matches 
        # Or if the reaction has other links to matches and is linked to any of the matched links
        # If not, skip the reaction
        if match_id_results \
            and (possible_reaction.match_link_id and possible_reaction.match_link_id not in match_id_results \
                  or possible_reaction.other_match_link_ids and not any(matched in possible_reaction.other_match_link_ids for matched in match_id_results)):
            continue
        # List of reactions in random order
        reactions_list = sample(possible_reaction.reactions, len(possible_reaction.reactions))
        if possible_reaction.react_only_one: # If only one of the possible reactions should be added
            await add_reaction(message, choice(reactions_list))
        else:
            for reaction in reactions_list:
                if possible_reaction.react_with_all: # If all of the possible reactions should be added
                    await add_reaction(message, reaction)
                else: # If the reaction should be added with a certain chance
                    if mock_bernoulli(possible_reaction.chance):
                        await add_reaction(message, reaction)

async def add_reaction(message: Message, reaction: str) -> None:
    try:
        await message.add_reaction(reaction)
    except Exception as e:
        print('Failed to react to message:', e, reaction)

async def reply_to_message(message: Message, replies: list[ReactReply]) -> None:
    for reply in replies:
        try:
            if mock_bernoulli(reply.chance):
                # TODO: Handle different types of replies
                await message.reply(reply.message)
        except Exception as e:
            print('Failed to reply to message:', e, reply)


async def handle_message_react(message: Message)  -> list[str]:
    events = []
    for event_name, resource in REACT_RESOURCES.items():
        match_results = check_matches(message.content, resource.matches)
        if bool(match_results):
            # If the match results are not a set, it means that there was a match but no link IDs were found
            if not isinstance(match_results, set):
                match_results = None
            if resource.possible_reactions:
                await react_to_message(message, resource.possible_reactions, match_results)
            if resource.replies:
                await reply_to_message(message, resource.replies)
            events.append(event_name)
            
    return events