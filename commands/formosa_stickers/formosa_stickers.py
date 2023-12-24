import discord
from discord import app_commands
from discord.app_commands import Choice
import random

from ..modules import logging

from .consts import STYLE_TYPE_CHOICES, TAGS, TYPE_CHOICES
from .functions import fetch_sticker, fetch_stickers_list
FETCHED_TIMEOUT = 21600 # once every 6 hours

def register_commands(tree, guilds: list[discord.Object]):

    async def send_sticker(interaction: discord.Interaction, user: discord.User = None, 
                           type: str = 'search', style: str | None = None, query: str | None = None, 
                           latest: bool = False):
        await interaction.response.defer()

        # get the sticker urls
        stickers_list = fetch_stickers_list(type, style, query)

        if (latest):
            sticker = stickers_list[0]
        else:
            sticker = random.choice(stickers_list)

        sticker_name = sticker['url'].split('/')[-1].split('.')[0]
        sticker_url = sticker['url']
        # fetch the image and get as discord file
        file = discord.File(fetch_sticker(sticker_url), filename=f'{sticker_name}.{"gif" if sticker["type"] == "gif" else "jpg"}')
        await interaction.followup.send(f"<@{user.id}>" if user else None, file=file, ephemeral=True)

        log_event = {
            "event": "sticker",
            "author_id": interaction.user.id,
            "mentioned_id": user.id if user else None,
            "metadata": {
                'type': type,
                'style': style,
                'query': query,
                "latest": latest,
            }
        }

        await logging.log_event(interaction, log_event, content=sticker, log_to_channel=False)

    sticker_group = app_commands.Group(name="stickers", description="Boomer stickers from https://sticker.fpg.com.tw/")

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
    async def search(interaction: discord.Interaction, user: discord.User = None, type: Choice[str] = None, style: Choice[str] = None, query: str = None, latest: bool = True):
        await send_sticker(interaction, user, type.value if type else 'search', style.value if style else None, query, latest)

    tree.add_command(sticker_group, guilds=guilds)