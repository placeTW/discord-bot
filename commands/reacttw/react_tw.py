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
    "<:TWHW3:1139172056349548604>",
    "<:rice_cooker:1139169683824713892>",
    "<:tw_beer:1139314162615459942>",
    "<:hilife:1139176380521791519>",
    "<:tw_hw_3:1139172056349548604>",
)


def is_TW_message(message: discord.Message):
    to_upper = message.content.upper()
    return (
        ("TAIWAN" in to_upper)
        or ("FORMOSA" in to_upper)
        or ("台灣" in message.content)
        or ("臺灣" in message.content)
        or ("FORMOSA" in to_upper)
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
        if mock_bernoulli(0.15):
            await message.add_reaction(react)
