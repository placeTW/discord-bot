import discord
import os
import aiohttp
import asyncio

API_KEY = os.getenv("MODERATE_CONTENT_API_KEY")
API_URL = 'https://api.moderatecontent.com/moderate/'


# https://www.moderatecontent.com/documentation/content
async def review_image(file: discord.Attachment) -> bool:
    # Note: API key in URL is required by ModerateContent API
    # See: https://www.moderatecontent.com/documentation/
    url = f'{API_URL}?key={API_KEY}&url={file.url}'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                # convert response to json
                data = await response.json()
                # check if image is safe (rating of everyone)
                return data.get('rating_index') == 1
    except (aiohttp.ClientError, asyncio.TimeoutError, KeyError) as e:
        print(f"Content moderation API error: {e}")
        return False
