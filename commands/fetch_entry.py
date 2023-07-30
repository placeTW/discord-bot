import aiohttp
import discord
from discord import app_commands


async def _async_get_json(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            # print("Status:", response.status)
            # print("Content-type:", response.headers['content-type'])
            json_response = await response.json()
    return json_response


def register_commands(tree, this_guild: discord.Object):
    @tree.command(
        name="fetch",
        description="Fetches something idk",
        guild=this_guild,
    )
    @app_commands.describe(index="a number between 0 and 15, should be changed later")
    async def fetch_entry(interaction: discord.Interaction, index: int):
        result_json = await _async_get_json(
            "https://placetw.com/locales/en/art-pieces.json"
        )
        await interaction.response.send_message(
            f"Here: `{result_json[index]['title']}`"
        )


if __name__ == "__main__":
    import asyncio

    asyncio.run(_async_get_json("https://placetw.com/locales/en/art-pieces.json"))
