import discord
import random
from .consts import POSSIBLE_REACTS, TW_REGEX


def is_TW_message(message: discord.Message):
    return TW_REGEX.search(message.content.upper())


def mock_bernoulli(p: float) -> bool:
    """Returns True with probability p.

    Args:
        p (float): a float between 0 and 1.

    Returns:
        bool: True or False.
    """
    return random.random() < p


async def send_react_tw(message: discord.Message):
    for react in POSSIBLE_REACTS:
        if mock_bernoulli(0.15):
            await message.add_reaction(react)
