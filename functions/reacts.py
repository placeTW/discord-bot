from enum import StrEnum
import json
from operator import and_, not_, or_
from pathlib import Path
from pydantic import BaseModel
from re import search, IGNORECASE, UNICODE
from discord import Message
from random import sample
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

# An event that can be triggered by a message that matches the criteria.
class ReactEvent(BaseModel):
    # The condition to evaluate if the event should be triggered. A boolean expression that takes criteria links as operands.
    condition: str = "True"
    # The chance that the reaction/reply will be triggered. A float between 0 and 1.
    chance: float


class ReactEventReaction(ReactEvent):
    # A list of reactions that can be added to the message.
    reactions: list[str]
    # Whether all of the possible reactions should be added to the message.
    react_with_all: bool = False
    # The maximum number of reactions that can be added to the message. If -1, there is no limit.
    max_react_limit: int = -1

class ReactEventReply(ReactEvent):
    # The reply message that can be sent.
    message: str
    # The type of the reply message.
    type: ReactReplyType = "text"
    # How many times the reply message can be sent.
    multiplier: int = 1
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

def check_matches(message_content: str, criteria: list[ReactCriteria]) -> bool | set[str]:
    criteria_links = set()
    found_match = False
    for possible_match in criteria:
        if possible_match.match_whole_word:
            if search(rf"\b(?:{'|'.join(possible_match.keywords)})\b", message_content, flags=IGNORECASE | UNICODE):
                found_match = True
                if possible_match.criteria_link:
                    criteria_links.add(possible_match.criteria_link)
        else:
            if search(rf"{'|'.join(possible_match.keywords)}", message_content, flags=IGNORECASE | UNICODE):
                found_match = True
                if possible_match.criteria_link:
                    criteria_links.add(possible_match.criteria_link)
    # If no link IDs were found, return if there was a match
    return criteria_links if len(criteria_links) > 0 else found_match

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
                    col_offset=node.col_offset
                )
            return node
    
    transformed_expr = LinkIdTransformer().visit(parsed_expr)
    
    # Fix the AST by adding missing attributes
    ast.fix_missing_locations(transformed_expr)
    
    compiled_expr = compile(transformed_expr, '<string>', 'eval')
    return eval(compiled_expr, {"__builtins__": {}}, allowed_names | {'link_id_exists': link_id_exists})




async def react_to_message(message: Message, possible_reactions: list[ReactEventReaction], match_id_results: set[str] = None) -> None:
    for possible_reaction in possible_reactions:
        # If the matched linked results exists check if the reaction is linked to a match
        if not evaluate_event_condition(possible_reaction.condition, match_id_results):
            continue
        # List of reactions in random order
        reactions_list = sample(possible_reaction.reactions, len(possible_reaction.reactions))
        reaction_count = 0
        for reaction in reactions_list:
            if possible_reaction.react_with_all: # If all of the possible reactions should be added
                await add_reaction(message, reaction)
                reaction_count += 1
            elif possible_reaction.max_react_limit > 0 and reaction_count >= possible_reaction.max_react_limit:
                break
            else: # If the reaction should be added with a certain chance
                if mock_bernoulli(possible_reaction.chance):
                    await add_reaction(message, reaction)
                    reaction_count += 1

async def add_reaction(message: Message, reaction: str) -> None:
    try:
        await message.add_reaction(reaction)
    except Exception as e:
        print('Failed to react to message:', e, reaction)

async def reply_to_message(message: Message, possible_replies: list[ReactEventReply], match_id_results: set[str] = None) -> None:
    for possible_reply in possible_replies:
        # If the matched linked results exists check if the reply is linked to a match
        if not evaluate_event_condition(possible_reply.condition, match_id_results):
            continue
        try:
            if mock_bernoulli(possible_reply.chance):
                # TODO: Handle different types of replies
                await message.reply(possible_reply.message, mention_author=possible_reply.mention_author)
        except Exception as e:
            print('Failed to reply to message:', e, possible_reply)


async def handle_message_react(message: Message)  -> list[str]:
    events = []
    for event_name, resource in REACT_RESOURCES.items():
        match_results = check_matches(message.content, resource.criteria)
        if bool(match_results):
            # If the match results are not a set, it means that there was a match but no link IDs were found
            # All the possible reactions/replies will be used in this case
            if not isinstance(match_results, set):
                match_results = None
            if resource.possible_reactions:
                await react_to_message(message, resource.possible_reactions, match_results)
            if resource.possible_replies:
                await reply_to_message(message, resource.possible_replies)
            events.append(event_name)
            
    return events
