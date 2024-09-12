import aiohttp


async def _async_get_json(url: str) -> str:
    """An async version of getting a JSON file.
    This is because discord doesn't like it when
    you use blocking IO (non async) for HTTP requests,
    since the entire bot will not do anything until
    the HTTP request is fulfilled.

    Args:
        url (str): _description_

    Returns:
        str: _description_
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()
