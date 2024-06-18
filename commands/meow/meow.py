from random import choice, randint, shuffle
import discord

from modules.probability import mock_bernoulli
from .consts import (
    CHISOBCAT,
    MEOW,
    MEOW_REGEX,
    POSSIBLE_MEOW_MESSAGES,
    POSSIBLE_MEOW_REACTS,
    SHIBELOL,
    TRADITIONAL_CAT,
)


def is_meow_message(message: discord.Message):
    return MEOW_REGEX.search(message.content)


def is_traditional_cat(message: discord.Message):
    return TRADITIONAL_CAT in message.content


def from_meow_channel(message: discord.Message):
    return MEOW in message.channel.name


async def do_meow(
    message: discord.Message, mention_author=False, multiplier=1
):
    if not mention_author and mock_bernoulli(0.75):
        await message.channel.send(choice(POSSIBLE_MEOW_MESSAGES))
    else:
        await message.reply(MEOW * multiplier, mention_author=mention_author)


async def react_meow(message: discord.Message):
    shuffle(POSSIBLE_MEOW_REACTS)
    for react in POSSIBLE_MEOW_REACTS:
        if mock_bernoulli(0.25):
            await message.add_reaction(react)


async def shibelol(message: discord.Message):
    if mock_bernoulli(0.5):
        await message.add_reaction(CHISOBCAT)
    if mock_bernoulli(0.1):
        await message.reply(SHIBELOL)


async def meow_meow(message: discord.Message):
    if is_meow_message(message):
        await react_meow(message)
        return True

    if is_traditional_cat(message):
        await do_meow(message, multiplier=randint(2, 101))
        return True
    elif is_meow_message(message) and mock_bernoulli(0.169):
        await do_meow(message, multiplier=randint(1, 5))
        return True
    elif from_meow_channel(message) and not is_meow_message(message):
        await shibelol(message)
    elif mock_bernoulli(0.001):
        await do_meow(message)
        return True

    return False
