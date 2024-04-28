from re import compile, IGNORECASE, UNICODE
import discord
from ..modules.probability import mock_bernoulli

KEYWORDS_EARTHQUAKE = {
  'earthquake',
  '地震',
  '這杯水在晃',
}

EARTHQUAKE_REGEX = compile(
    rf"\b(?:{'|'.join(KEYWORDS_EARTHQUAKE)})\b",
    flags=IGNORECASE | UNICODE,
)

def is_earthquake_message(message: discord.Message):
    return EARTHQUAKE_REGEX.search(message.content)

async def send_react_earthquake(message: discord.Message):
    if mock_bernoulli(0.90):
        await message.reply("https://www.youtube.com/watch?v=P24eOUl46k0")