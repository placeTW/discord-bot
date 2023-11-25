import discord
import os
from dotenv import load_dotenv
import requests
load_dotenv()

API_KEY = os.getenv("MODERATE_CONTENT_API_KEY")
API_URL = 'https://api.moderatecontent.com/moderate/'

# https://www.moderatecontent.com/documentation/content
async def review_image(file: discord.Attachment) -> bool:
  url = f'{API_URL}?key={API_KEY}&url={file.url}'
  try:
    # send a get request
    response = requests.get(url)
    # convert response to json
    data = response.json()
    print(data)
    # check if image is safe (rating of everyone)
    return data['rating_index'] == 1
  except:
    return False