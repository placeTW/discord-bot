# credits: https://github.com/pytest-dev/pytest-asyncio/issues/30#issuecomment-226947196
import asyncio, pytest
import os


@pytest.fixture
def event_loop():
    """Create an instance of the default event loop for each test case."""
    policy = (
        asyncio.WindowsSelectorEventLoopPolicy()
        if os.name == "nt"
        else asyncio.DefaultEventLoopPolicy()
    )
    res = policy.new_event_loop()
    asyncio.set_event_loop(res)
    res._close = res.close
    res.close = lambda: None

    yield res

    res._close()
