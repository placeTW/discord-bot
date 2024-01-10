import discord
from discord import app_commands
from discord.app_commands import Choice

from .consts import STYLE_TYPE_CHOICES, TAGS, TYPE_CHOICES
from .functions import send_sticker
FETCHED_TIMEOUT = 21600 # once every 6 hours

def register_commands(tree, guilds: list[discord.Object]):

    sticker_group = app_commands.Group(name="stickers", description="Boomer stickers from https://sticker.fpg.com.tw/")

    # Good morning command
    @sticker_group.command(
        name="goodmorning",
        description="Good morning stickers"
    )
    @app_commands.describe(user='The user to ping')
    @app_commands.describe(latest='Get the latest sticker (random if false)')
    @app_commands.describe(style='The style of the sticker')
    @app_commands.choices(style=STYLE_TYPE_CHOICES)
    async def good_morning(interaction: discord.Interaction, user: discord.User = None, style: Choice[str] = None, latest: bool = False):
        await send_sticker(interaction, user, 'daily', style.value if style else None, TAGS['morning'], latest)

    # Good night command
    @sticker_group.command(
        name="goodnight",
        description="Good night stickers"
    )
    @app_commands.describe(user='The user to ping')
    @app_commands.describe(latest='Get the latest sticker (random if false)')
    @app_commands.describe(style='The style of the sticker')
    @app_commands.choices(style=STYLE_TYPE_CHOICES)
    async def good_night(interaction: discord.Interaction, user: discord.User = None, style: Choice[str] = None, latest: bool = False):
        await send_sticker(interaction, user, 'daily', style.value if style else None, TAGS['night'], latest)

    # Happy holidays command
    @sticker_group.command(
        name="happyholidays",
        description="Happy holidays stickers"
    )
    @app_commands.describe(user='The user to ping')
    @app_commands.describe(latest='Get the latest sticker (random if false)')
    @app_commands.describe(style='The style of the sticker')
    @app_commands.choices(style=STYLE_TYPE_CHOICES)
    async def happy_holidays(interaction: discord.Interaction, user: discord.User = None, style: Choice[str] = None, latest: bool = False):
        await send_sticker(interaction, user, 'search', style.value if style else None, TAGS['happy_holidays'], latest)

    # New year command
    @sticker_group.command(
        name="newyear",
        description="New year stickers"
    )
    @app_commands.describe(user='The user to ping')
    @app_commands.describe(latest='Get the latest sticker (random if false)')
    @app_commands.describe(style='The style of the sticker')
    @app_commands.choices(style=STYLE_TYPE_CHOICES)
    async def new_year(interaction: discord.Interaction, user: discord.User = None, style: Choice[str] = None, latest: bool = False):
        await send_sticker(interaction, user, 'search', style.value if style else None, TAGS['new_year'], latest)

    # Search command
    @sticker_group.command(
        name="search",
        description="Searches for stickers from the website"
    )
    @app_commands.describe(user='The user to ping')
    @app_commands.describe(latest='Get the latest sticker (random if false, default true)')
    @app_commands.describe(style='The style of the sticker')
    @app_commands.choices(style=STYLE_TYPE_CHOICES)
    @app_commands.describe(type='The type of sticker')
    @app_commands.choices(type=TYPE_CHOICES)
    @app_commands.describe(query='The tags to search for (in Traditional Chinese, separated by commas)')
    async def search(interaction: discord.Interaction, user: discord.User = None, query: str = None, type: Choice[str] = None, style: Choice[str] = None, latest: bool = False):
        await send_sticker(interaction, user, type.value if type else 'search', style.value if style else None, query, latest)

    tree.add_command(sticker_group, guilds=guilds)