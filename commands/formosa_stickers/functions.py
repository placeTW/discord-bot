from bs4 import BeautifulSoup
import urllib3
from io import BytesIO
import random
import discord

from modules import logging

from .consts import POSSIBLE_URLS, SITE_URL

def get_url(type: str, style: str | None, query: str | None):
    query_params = []
    if style:
        query_params.append(f'style={style}')
    if query:
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
        stickers = [{
            'url': item.find('img')['data-original'],
            'type': item['data-partern'],
        } for item in items]

        return stickers
    except:
        return []
    
def fetch_sticker(sticker_url):
    http = urllib3.PoolManager()
    response = http.request('GET', f'{SITE_URL}/{sticker_url}')
    data = response.data
    return BytesIO(data)


async def send_sticker(interaction: discord.Interaction, user: discord.User = None, 
                        type: str = 'search', style: str | None = None, query: str | None = None, 
                        latest: bool = False):
    await interaction.response.defer()

    # get the sticker urls
    stickers_list = fetch_stickers_list(type, style, query)
    if (len(stickers_list) == 0):
        await interaction.followup.send(f"No stickers found for query: {query}", ephemeral=True)
        return

    if (latest):
        sticker = stickers_list[0]
    else:
        sticker = random.choice(stickers_list)

    sticker_name = sticker['url'].split('/')[-1].split('.')[0]
    sticker_url = sticker['url']
    # fetch the image and get as discord file
    file = discord.File(fetch_sticker(sticker_url), filename=f'{sticker_name}.{"gif" if "gif" in sticker["type"] else "jpg"}')
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