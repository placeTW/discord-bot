import discord
import random
from .consts import POSSIBLE_REACTS, BALTIC_REGEX


def is_baltic_message(message: discord.Message):
    return BALTIC_REGEX.search(message.content)


def mock_bernoulli(p: float) -> bool:
    """Returns True with probability p.

    Args:
        p (float): a float between 0 and 1.

    Returns:
        bool: True or False.
    """
    return random.random() < p


async def send_react_baltic(message: discord.Message):
    for react in POSSIBLE_REACTS:
        if mock_bernoulli(0.69):
            await message.add_reaction(react)
