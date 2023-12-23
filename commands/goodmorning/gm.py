from bs4 import BeautifulSoup
import urllib3
import time
import discord
from discord import app_commands
import random
from PIL import Image
from io import BytesIO
from ..modules import logging

SITE_URL = 'https://sticker.fpg.com.tw'
DAILY_URL = f'{SITE_URL}/daily.aspx?keywords=%E6%97%A9%E5%AE%89'
FETCHED_TIMEOUT = 86400

def fetch():
    http = urllib3.PoolManager()
    response = http.request('GET', DAILY_URL)
    data = response.data.decode('utf-8')

    soup = BeautifulSoup(data, 'html.parser')

    # get all items with the class grid-item wow
    items = soup.find_all('a', class_='grid-item wow')

    # get the urls of all the images
    urls = [item.find('img')['data-original'] for item in items]

    return urls
    

def register_commands(tree, guilds: list[discord.Object]):
    state = {
        "last_fetched_timestamp": time.time(),
        "sticker_urls": fetch(),
    }

    @tree.command(
        name="goodmorning",
        description="Good morning stickers",
        guilds=guilds,
    )
    @app_commands.describe(daily='Get the daily sticker (random if false)')
    async def good_morning(interaction: discord.Interaction, daily: bool = False):
        await interaction.response.defer()
        current_time = time.time()
        time_difference = current_time - state["last_fetched_timestamp"]
        if (time_difference > FETCHED_TIMEOUT):
            state["sticker_urls"] = fetch()
            state["last_fetched_timestamp"] = current_time
            print("Fetched new stickers")

        if (daily):
            sticker_url = state["sticker_urls"][0]
        else:
            sticker_url = random.choice(state["sticker_urls"])

        # fetch the image and get as discord file
        # the response is
        http = urllib3.PoolManager()
        response = http.request('GET', f'{SITE_URL}/{sticker_url}')
        data = response.data

        # send to discord
        file = discord.File(BytesIO(data), filename=sticker_url.split('/')[-1])
        await interaction.followup.send(file=file)

        log_event = {
            "event": "goodmorning",
            "author_id": interaction.user.id,
            "metadata": {
                "daily": daily,
                'sticker_url': sticker_url
            },
        }

        await logging.log_event(interaction, log_event, log_to_channel=False)
