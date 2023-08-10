from commands.shiba import random_shiba
import requests


async def test_dog_api():
    """
    If something is wrong with their API, we either need
    to adjust it or get rid of it entirely.
    """
    for link in random_shiba.POSSIBLE_BREEDS:
        result = await random_shiba.get_shiba(link)
        assert result["status"] == "success"
