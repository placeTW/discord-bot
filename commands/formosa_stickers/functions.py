from bs4 import BeautifulSoup
import urllib3
from io import BytesIO

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