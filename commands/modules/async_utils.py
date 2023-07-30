import aiohttp


async def _async_get_json(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print("Status:", response.status)
            print("Content-type:", response.headers["content-type"])
            if response.headers["content-type"] != "application/json":
                return None
            return await response.json()
