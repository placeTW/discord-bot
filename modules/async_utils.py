import aiohttp


async def _async_get_json(url: str, expected_content_type='application/json', headers: dict = None) -> str:
    """An async version of getting a JSON file.
    This is because discord doesn't like it when
    you use blocking IO (non async) for HTTP requests,
    since the entire bot will not do anything until
    the HTTP request is fulfilled.

    Args:
        url (str): _description_
        expected_content_type: passed to response.json(). Use None to disable content type checking.
        headers: optional HTTP headers to include in the request.

    Returns:
        str: _description_
    """
    timeout = aiohttp.ClientTimeout(total=10)  # 10 second timeout
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url,
            timeout=timeout,
            max_redirects=5,  # Limit redirect chains
            allow_redirects=True,
            headers=headers,
        ) as response:
            response.raise_for_status()

            # Validate response size (prevent memory exhaustion)
            content_length = response.headers.get('Content-Length')
            if content_length and int(content_length) > 10 * 1024 * 1024:  # 10MB limit
                raise ValueError("Response too large")

            # Read and parse JSON with size validation
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
    timeout = aiohttp.ClientTimeout(total=10)  # 10 second timeout
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url,
            timeout=timeout,
            max_redirects=5,  # Limit redirect chains
            allow_redirects=True
        ) as response:
            # if response returns 404, return None
            if response.status == 404:
                return None

            response.raise_for_status()

            # Validate response size (prevent memory exhaustion)
            content_length = response.headers.get('Content-Length')
            if content_length and int(content_length) > 10 * 1024 * 1024:  # 10MB limit
                raise ValueError("Response too large")

            # Read with size limit check
            content = await response.text()
            if len(content) > 10 * 1024 * 1024:
                raise ValueError("Response too large")

            return content