import time
import discord
from ..modules import logging
from discord import app_commands


GO_THE_FUCK_TO_SLEEP_URL = "https://www.youtube.com/watch?v=teIbh8hFQos"
COOLDOWN_DURATION = 60


def register_commands(tree, guilds: list[discord.Object]):
    user_timestamps: dict[int, float] = {}

    @tree.command(
        name="gothefucktosleep",
        description="Go the fuck to sleep",
        guilds=guilds,
    )
    @app_commands.rename(user_to_ping='member')
    async def go_the_fuck_to_sleep(interaction: discord.Interaction, user_to_ping: discord.Member):
        current_user_id = interaction.user.id
        current_time = time.time()
        time_difference = current_time - \
            (user_timestamps[current_user_id]
             if current_user_id in user_timestamps else 0)
        if (time_difference < COOLDOWN_DURATION):
            await interaction.response.send_message(f"<@{current_user_id}> https://www.youtube.com/watch?v=teIbh8hFQos (cooldown: {round(COOLDOWN_DURATION - time_difference)}s)")
            return

        await interaction.response.send_message(f"<@{user_to_ping.id}> https://www.youtube.com/watch?v=teIbh8hFQos")

        log_event = {
            "event": "gothefucktosleep",
            "author_id": current_user_id,
            "mentioned_id": user_to_ping.id,
        }
        
        await logging.log_event(interaction, log_event, log_to_channel=False)
        user_timestamps[current_user_id] = current_time
