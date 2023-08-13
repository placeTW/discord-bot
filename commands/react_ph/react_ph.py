import discord
import random
from .consts import POSSIBLE_REACTS, PH_REGEX
from ..modules.probability import mock_bernoulli


def is_ph_message(message: discord.Message):
    return PH_REGEX.search(message.content)


async def send_react_ph(message: discord.Message):
    for react in POSSIBLE_REACTS:
        if mock_bernoulli(0.69):
            await message.add_reaction(react)
