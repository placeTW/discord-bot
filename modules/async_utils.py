import aiohttp


async def _async_get_json(url: str, expected_content_type='application/json') -> str:
    """An async version of getting a JSON file.
    This is because discord doesn't like it when
    you use blocking IO (non async) for HTTP requests,
    since the entire bot will not do anything until
    the HTTP request is fulfilled.

    Args:
        url (str): _description_
        expected_content_type: passed to response.json(). Use None to disable content type checking.

    Returns:
        str: _description_
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json(content_type=expected_content_type)

async def _async_get_html(url: str) -> str:
    """An async version of getting a HTML file.
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
            # if response returns 404, return None
            if response.status == 404:
                return None
            return await response.text()