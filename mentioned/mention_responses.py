import random
import discord
from modules.probability import mock_bernoulli


# a dict of possible responses and their weights when the bot is mentioned.
POSSIBLE_RESPONSES_MAP = {
    "<:BocchiPing:1170161488812593172>": 4,
    "<:uwu:1161126694762061825>": 3,
    "<a:catArrive:1161441364869918881>": 3,
    "<:ChisobCat:1157361078452375582>": 2,
    "<:Black_Bear:1132603463126237244>": 1,
    "<:101_Top:1132608896222113951>\n<:101_Floor:1132608196515725332>": 1,
    "<:PineappleCake:1156373382565212323>": 1,
    "<:twslipper:1156375845330485298>": 1,
    "<:tw_amogus:1133361653908516885>": 1,
    "<:meow_b:1249076752798449817>": 1,
    "<:meow_o:1179052271175204894>": 1,
    "<:meow_g:1179047382193807370>": 1,
    "喵": 1,
    "🧋": 1,
    # from Baltics server
    "<:caveman:1131703579439284274>": 1,
}
RESPONSES = list(POSSIBLE_RESPONSES_MAP.keys())
WEIGHTS = list(POSSIBLE_RESPONSES_MAP.values())


def get_random_response() -> str:
    # ^ could also change k in the future to be a random number
    response = random.choices(RESPONSES, weights=WEIGHTS, k=1)[0]
    return response


async def reply_with_random_response(message: discord.Message):
    if mock_bernoulli(0.95):
        response = get_random_response()
        await message.reply(response)
