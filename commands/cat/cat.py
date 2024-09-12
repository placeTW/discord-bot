import discord
from modules.async_utils import _async_get_json
import os
from dotenv import load_dotenv

load_dotenv()

CAT_API_URL = "https://api.thecatapi.com/v1/images/search"
API_KEY = os.getenv("CAT_API_KEY")

async def get_cat():
    return await _async_get_json(f'{CAT_API_URL}?api_key={API_KEY}')

def register_commands(tree, guilds: list[discord.Object]):
    @tree.command(
        name="cat",
        description="Random cat image",
        guilds=guilds,
    )
    async def random_cat(
        interaction: discord.Interaction,
    ):
        cat_json = await get_cat()
        if cat_json is None:
            return await interaction.response.send_message("Sorry, we couldn't find any cats ):")
        await interaction.response.send_message(cat_json[0]["url"])
