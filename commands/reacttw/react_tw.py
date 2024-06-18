import discord
from .consts import POSSIBLE_REACTS, TW_REGEX
from modules.probability import mock_bernoulli


def is_TW_message(message: discord.Message):
    return TW_REGEX.search(message.content)


async def send_react_tw(message: discord.Message):
    for react in POSSIBLE_REACTS:
        if mock_bernoulli(0.125):
            await message.add_reaction(react)
    if mock_bernoulli(0.07):
        await message.reply("https://www.youtube.com/watch?v=AN0rQR0RlOM")
