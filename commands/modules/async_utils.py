import aiohttp


async def _async_get_json(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            # print("Status:", response.status)
            # print("Content-type:", response.headers['content-type'])
            json_response = await response.json()
    return json_response
