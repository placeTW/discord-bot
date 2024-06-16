import discord
from .consts import POSSIBLE_REACTS, CZECH_REGEX
from modules.probability import mock_bernoulli


def is_czech_message(message: discord.Message):
    return CZECH_REGEX.search(message.content)


async def send_react_czech(message: discord.Message):
    for react in POSSIBLE_REACTS:
        if mock_bernoulli(0.69):
            await message.add_reaction(react)
