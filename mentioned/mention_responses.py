import random
import discord

# a dict of possible responses and their weights when the bot is mentioned.
POSSIBLE_RESPONSES_MAP = {
    "<:BocchiPing:1170161488812593172>": 5,
    "<:uwu:1161126694762061825>": 3,
    "<a:catArrive:1161441364869918881>": 3,
    "<:ChisobCat:1157361078452375582>": 2,
    "<:Black_Bear:1132603463126237244>": 1,
    "<:101_Top:1132608896222113951>\n<:101_Floor:1132608196515725332>": 1,
    "<:PineappleCake:1156373382565212323>": 1,
    "<:slipper:1132961055304323143>": 1,
    "喵": 1,
    "🧋": 1,
}
RESPONSES = list(POSSIBLE_RESPONSES_MAP.keys())
WEIGHTS = list(POSSIBLE_RESPONSES_MAP.values())


def get_random_response() -> str:
    # ^ could also change k in the future to be a random number
    response = random.choices(RESPONSES, weights=WEIGHTS, k=1)[0]
    return response


async def reply_with_random_response(message: discord.Message):
    response = get_random_response()
    await message.reply(response)
