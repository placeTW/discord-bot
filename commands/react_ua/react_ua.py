import discord
from .consts import POSSIBLE_REACTS, UA_REGEX
from ..modules.probability import mock_bernoulli


def is_UA_message(message: discord.Message):
    return UA_REGEX.search(message.content)


async def send_react_ua(message: discord.Message):
    for react in POSSIBLE_REACTS:
        if mock_bernoulli(0.50):
            await message.add_reaction(react)
    if mock_bernoulli(0.50):
        await message.add_reaction("💙")
        await message.add_reaction("💛")
