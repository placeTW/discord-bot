"""
This file just tests if async functions work correctly,
and is not meant to be used in real testing.
"""
import asyncio


async def test_asyncio_sleep():
    await asyncio.sleep(0.01)
