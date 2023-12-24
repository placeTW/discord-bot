from bs4 import BeautifulSoup
import urllib3
import discord
from discord import app_commands
from discord.app_commands import Choice
import random
from io import BytesIO
from ..modules import logging

from .consts import SITE_URL, POSSIBLE_URLS, STYLE_TYPE_CHOICES, POSSIBLE_TAGS, TAGS
FETCHED_TIMEOUT = 21600 # once every 6 hours

def get_url(type: str, style: str | None, query: str | list(str) | None):
    query_params = []
    if style:
        query_params.append(f'style={style}')
    if query:
        if isinstance(query, list):
            query_params.append(f'keywords={",".join(query)}')
        else:
            query_params.append(f'keywords={query}')
    query_str = '&'.join(query_params)
    return f'{POSSIBLE_URLS[type]}?{query_str}'

def fetch_stickers_list(type: str, style: str, query: str):
    try:
        http = urllib3.PoolManager()
        response = http.request('GET', get_url(type, style, query))
        data = response.data.decode('utf-8')

        soup = BeautifulSoup(data, 'html.parser')

        # get all items with the class grid-item wow
        items = soup.find_all('a', class_='grid-item wow')

        # get the urls of all the images
        urls = [{
            'url': item.find('img')['data-original'],
            'type': item['data-partern'],
        } for item in items]

        return urls
    except:
        return []
    
def fetch_sticker(sticker_url):
    http = urllib3.PoolManager()
    response = http.request('GET', f'{SITE_URL}/{sticker_url}')
    data = response.data
    return BytesIO(data)


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

    tree.add_command(sticker_group, guilds=guilds)