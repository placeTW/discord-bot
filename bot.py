from typing import Any
import discord
from presence import watching
from discord.ext import tasks

CHANGE_STATUS_INTERVAL_HOURS = 1


class TWPlaceClient(discord.Client):
    def __init__(self, *args, **kwargs) -> None:
        intents = discord.Intents.default()
        # also turn on messages functionality
        intents.message_content = True
        movie_activity = watching.get_random_movie_as_activity()
        super().__init__(
            intents=intents, activity=movie_activity, *args, **kwargs
        )

    @tasks.loop(hours=CHANGE_STATUS_INTERVAL_HOURS)
    async def set_watching_status(self):
        movie_activity = watching.get_random_movie_as_activity()
        await self.change_presence(
            status=discord.Status.idle, activity=movie_activity
        )

    @set_watching_status.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in

    async def setup_hook(self) -> None:
        # start the task to run in the background
        self.set_watching_status.start()


def get_bot():
    client = TWPlaceClient()
    return client
