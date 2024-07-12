from typing import Any
import discord
from activities import activity
from discord.ext import tasks
from modules.config import fetch_config

CHANGE_STATUS_INTERVAL_HOURS = 1


class TWPlaceClient(discord.Client):
    def __init__(self, is_prod: bool, *args, **kwargs) -> None:
        intents = discord.Intents.default()
        # also turn on messages functionality
        intents.message_content = True
        movie_activity = activity.get_random_activity_as_discordpy_activity()
        # config
        self.is_prod = is_prod
        self.guilds_dict = fetch_config(is_prod)
        super().__init__(
            intents=intents, activity=movie_activity, *args, **kwargs
        )

    @tasks.loop(hours=CHANGE_STATUS_INTERVAL_HOURS)
    async def set_activity(self):
        random_activity = activity.get_random_activity_as_discordpy_activity()
        await self.change_presence(activity=random_activity)

    @set_activity.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in

    async def setup_hook(self) -> None:
        # start the task to run in the background
        self.set_activity.start()

    def fetch_config(self):
        self.guilds_dict = fetch_config(self.is_prod)


def get_bot(is_prod: bool):
    client = TWPlaceClient(is_prod)
    return client
