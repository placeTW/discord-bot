import discord
import random

POSSIBLE_REACTS = (
    "<:flag_twi:1133045891780071436>",
    "<:Black_Bear:1132603463126237244>",
    "<:Urocissacaerulea:1132839946303062086>",
    "<:101_Floor:1132608196515725332>",
    "<:tw_amogus:1133361653908516885>",
    "<:roc_troll:1133368648967405610>",
    "<:roc_heart:1133045894678319235>",
    "<:tw_heart:1133045893227102299>",
    "<:bubblemilktea:1132632348651966596>",
)


def is_TW_message(message: discord.Message):
    return (
        ("TAIWAN" in message.content.upper())
        or ("台灣" in message.content)
        or ("臺灣" in message.content)
    )


def mock_bernoulli(p: float) -> bool:
    """Returns True with probability.

    Args:
        p (float): a float between 0 and 1.

    Returns:
        bool: True or False.
    """
    return random.random() < p


async def send_react_tw(message: discord.Message):
    for react in POSSIBLE_REACTS:
        if mock_bernoulli(0.25):
            await message.add_reaction(react)
