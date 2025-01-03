from enum import StrEnum
import json
from operator import and_, not_, or_
from pathlib import Path
from pydantic import BaseModel
from re import search, IGNORECASE, UNICODE
from discord import Message
from random import randint, sample
import ast

from modules.probability import mock_bernoulli


class ReactReplyType(StrEnum):
    text = "text"
    image = "image"
    video = "video"
    audio = "audio"
    file = "file"


class ReactCriteria(BaseModel):
    # A list of keywords that the message can contain. Supports regex.
    keywords: list[str]
    # Whether the keywords should match the whole word or not.
    match_whole_word: bool = False
    # The link ID of the criteria. This ID can be used for boolean expressions in the event condition.
    criteria_link: str = ""
    # A list of words that the channel name could contain for the message to match the criteria.
    channel_name_contains: list[str] = []


class ReactMessage(BaseModel):
    # The reply message that can be sent.
    message: str
    # The type of the reply message.
    type: ReactReplyType = "text"


# An event that can be triggered by a message that matches the criteria.
class ReactEvent(BaseModel):
    # The condition to evaluate if the event should be triggered. A boolean expression that takes criteria links as operands.
    condition: str = "True"
    # The chance that the reaction/reply will be triggered. A float between 0 and 1.
    chance: float
    # The content of the event
    content: str | list[str] | ReactMessage | list[ReactMessage]
    # The maximum number of reactions/replies that can be added to the message.
    max_limit: int = -1


class ReactEventReaction(ReactEvent):
    # Whether all of the possible reactions should be added to the message.
    react_with_all: bool = False


class ReactEventReply(ReactEvent):
    # How many times the reply message could be sent.
    random_multiplier: int = 1
    # Whether the author of the message should be mentioned in the reply.
    mention_author: bool = False


class ReactResource(BaseModel):
    # A list of objects that define the criteria for a message to match the reaction. A message can match any of the criteria to trigger the possible responses.
    criteria: list[ReactCriteria]
    # A list of possible reactions that can be added to the message.
    possible_reactions: list[ReactEventReaction] | None = None
    # A list of possible replies that can be sent.
    possible_replies: list[ReactEventReply] | None = None


REACT_RESOURCES_DIR = Path(Path(__file__).parent, "..", "resources", "reacts")


def load_react_resources() -> dict[str, ReactResource]:
    resources = {}
    for file in REACT_RESOURCES_DIR.iterdir():
        if file.suffix != ".json":
            continue
        try:
            with open(file, mode="r", encoding="utf8") as f:
                filename = file.stem
                data = json.load(f)
                resources[filename] = ReactResource(**data)
        except Exception as e:
            print(f"Failed to load react resource {file}: {e}")
    return resources


REACT_RESOURCES: dict[str, ReactResource] = load_react_resources()


# For testing in pytest to test a specific resource
def check_resource_match(message_content: str, resource_name: str) -> bool:
    resource = REACT_RESOURCES[resource_name]
    matches = check_matches(message_content, resource.criteria)
    return bool(matches)


def regex_search(message_content: str, possible_match: ReactCriteria) -> bool:
    if possible_match.match_whole_word:
        if search(rf"\b(?:{'|'.join(possible_match.keywords)})\b", message_content, flags=IGNORECASE | UNICODE):
            return True
    else:
        if search(rf"{'|'.join(possible_match.keywords)}", message_content, flags=IGNORECASE | UNICODE):
            return True
    return False


def check_matches(message_content: str, criteria: list[ReactCriteria], channel_name: str = "") -> bool | set[str]:
    criteria_links = set()
    found_match = False
    for possible_match in criteria:
        if channel_name and possible_match.channel_name_contains:
            if not search(
                rf"{'|'.join(possible_match.channel_name_contains)}", channel_name, flags=IGNORECASE | UNICODE
            ):
                continue
        if regex_search(message_content, possible_match):
            found_match = True
            if possible_match.criteria_link:
                criteria_links.add(possible_match.criteria_link)
    # If no link IDs were found, return if there was a match
    return criteria_links if len(criteria_links) > 0 else found_match


async def react_to_message(
    message: Message, possible_reactions: list[ReactEventReaction], criteria_links: set[str] = None
) -> bool:
    reaction_happened = False
    for possible_reaction in possible_reactions:
        # If the matched linked results exists check if the reaction is linked to a match
        if not evaluate_event_condition(possible_reaction.condition, criteria_links):
            continue
        # List of reactions in random order
        reactions_list = (
            sample(possible_reaction.content, len(possible_reaction.content))
            if isinstance(possible_reaction.content, list)
            else [possible_reaction.content]
        )
        reaction_count = 0
        for reaction in reactions_list:
            if possible_reaction.react_with_all:  # If all of the possible reactions should be added
                if await add_reaction(message, reaction):
                    reaction_happened = True
                    reaction_count += 1
            elif possible_reaction.max_limit > 0 and reaction_count >= possible_reaction.max_limit:
                break
            else:  # If the reaction should be added with a certain chance
                if mock_bernoulli(possible_reaction.chance):
                    if await add_reaction(message, reaction):
                        reaction_happened = True
                        reaction_count += 1
    return reaction_happened


async def add_reaction(message: Message, reaction: str) -> bool:
    try:
        await message.add_reaction(reaction)
        return True
    except Exception as e:
        print('Failed to react to message:', e, reaction)
        return False


async def reply_to_message(
    message: Message, possible_replies: list[ReactEventReply], criteria_links: set[str] = None
) -> bool:
    reply_happened = False
    for possible_reply in possible_replies:
        # If the matched linked results exists check if the reply is linked to a match
        if not evaluate_event_condition(possible_reply.condition, criteria_links):
            continue
        try:
            if mock_bernoulli(possible_reply.chance):
                if isinstance(possible_reply.content, list):
                    reply_count = 0
                    for reply in possible_reply.content:
                        if possible_reply.max_limit > 0 and reply_count >= possible_reply.max_limit:
                            break
                        if await send_message(
                            message, reply, possible_reply.random_multiplier, possible_reply.mention_author
                        ):
                            reply_happened = True
                            reply_count += 1

                else:
                    if await send_message(
                        message, possible_reply.content, possible_reply.random_multiplier, possible_reply.mention_author
                    ):
                        reply_happened = True

        except Exception as e:
            print('Failed to reply to message:', e, possible_reply)
    return reply_happened


async def send_message(
    message: Message, content: str | ReactMessage, multiplier: int = 1, mention_author: bool = False
) -> bool:
    try:
        # TODO: Handle different types of replies
        reply: str = content.message if isinstance(content, ReactMessage) else content
        await message.reply(reply * randint(1, multiplier), mention_author=mention_author)
        return True
    except Exception as e:
        print('Failed to send message:', e, content)
        return False


async def handle_message_react(message: Message) -> list[str]:
    events = []
    for event_name, resource in REACT_RESOURCES.items():
        match_results = check_matches(message.content, resource.criteria, message.channel.name)
        if bool(match_results):
            event_happened = False
            # If the match results are not a set, it means that there was a match but no link IDs were found
            # All the possible reactions/replies will be used in this case
            if not isinstance(match_results, set):
                match_results = None
            # Process the events
            if resource.possible_reactions:
                event_happened = event_happened or await react_to_message(
                    message, resource.possible_reactions, match_results
                )
            if resource.possible_replies:
                event_happened = event_happened or await reply_to_message(
                    message, resource.possible_replies, match_results
                )
            # If any event happened, add the event name to the logging list
            if event_happened:
                events.append(event_name)

    return events


def evaluate_event_condition(condition: str, criteria_links: set[str] | None = None) -> bool:
    """
    Evaluates a boolean condition string against a set of match link IDs.

    This function takes a condition string containing boolean expressions and link IDs,
    and evaluates it based on the presence of those link IDs in the provided set.
    It supports boolean operations (and, or, not) and treats any unrecognized word
    as a potential link ID.

    Args:
        condition (str): A string containing a boolean expression with link IDs.
                         Example: "baltic_meows or (hgs and not tw)"
        criteria_links (set): A set of strings representing the active link IDs.

    Returns:
        bool: The result of evaluating the condition against the match_link_ids.

    Raises:
        SyntaxError: If the condition string contains invalid Python syntax.
        NameError: If an unrecognized operation is used in the condition.

    Example:
        >>> match_link_ids = {'baltic_meows', 'tw'}
        >>> evaluate_condition("baltic_meows or hgs", match_link_ids)
        True
        >>> evaluate_condition("hgs and tw", match_link_ids)
        False

    Note:
        This function uses AST transformation to safely evaluate the condition
        without using eval() on raw input. It's designed to prevent arbitrary
        code execution while allowing flexible condition specifications.
    """
    if criteria_links is None:
        return True

    def link_id_exists(link_id):
        return link_id in criteria_links

    # Parse the condition string into an AST
    parsed_expr = ast.parse(condition, mode='eval')

    allowed_names = {
        'or': or_,
        'and': and_,
        'not': not_,
        'True': True,
        'False': False,
    }

    class LinkIdTransformer(ast.NodeTransformer):
        def visit_Name(self, node):
            if node.id not in allowed_names:
                return ast.Call(
                    func=ast.Name(id='link_id_exists', ctx=ast.Load()),
                    args=[ast.Constant(node.id)],
                    keywords=[],
                    lineno=node.lineno,
                    col_offset=node.col_offset,
                )
            return node

    transformed_expr = LinkIdTransformer().visit(parsed_expr)

    # Fix the AST by adding missing attributes
    ast.fix_missing_locations(transformed_expr)

    compiled_expr = compile(transformed_expr, '<string>', 'eval')
    return eval(compiled_expr, {"__builtins__": {}}, allowed_names | {'link_id_exists': link_id_exists})
