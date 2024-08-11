import discord
from random import choice

from commands.capoo.utils import get_videos_from_channel

CAPOO_YOUTUBE = "https://www.youtube.com/@BugCatCapoo/videos"
BASE_VIDEO_URL = 'https://www.youtube.com/watch?v='
BASE_SEARCH_URL = 'https://www.googleapis.com/youtube/v3/search?'


def register_commands(tree, guilds: list[discord.Object]):
    @tree.command(
        name="capoo",
        description="Get a random video from Capoo's YouTube channel",
        guilds=guilds,
    )
    async def random_capoo(
        interaction: discord.Interaction,
    ):
        video_links = get_videos_from_channel("UClr57MMpeX6m_p6hvvhu1Fw")
        await interaction.response.send_message(choice(video_links))
