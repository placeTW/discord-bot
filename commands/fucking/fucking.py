import time
import discord
from modules import logging
from discord import app_commands
from pathlib import Path
from random import randint


GO_THE_FUCK_TO_SLEEP_URLS = ["https://www.youtube.com/watch?v=teIbh8hFQos", # original
                             "https://www.youtube.com/watch?v=U08XWOx3XYM", # jennifer garner
                             "https://www.youtube.com/watch?v=G61kMUbpljY", # ani difranco
                             "https://www.youtube.com/watch?v=pgijPsNPbto", # werner herzog
                            #  "https://www.youtube.com/watch?v=VQ_WzkHRtX8", # age restricted (some old lady)
                             "https://www.youtube.com/watch?v=p2CHhuOlaH0", # lauren but it has a thanks for watching
                             "https://www.youtube.com/watch?v=aAGcalD-tNg", # jack sparrow
                             "https://www.youtube.com/watch?v=O51ZccrFeJQ"] # "That guy with a voice"
YOU_HAVE_TO_FUCKING_EAT_URL = "https://www.youtube.com/watch?v=ENdNzzJcB7Q"
MIKA_FUCKING_EAT_DIR = Path(Path(__file__).parent, "fuckingeatmika.png")
COOLDOWN_DURATION = 60


def register_commands(tree, guilds: list[discord.Object]):
    user_timestamps: dict[int, dict[str, float]] = {}

    @tree.command(
        name="gothefucktosleep",
        description="Go the fuck to sleep",
        guilds=guilds,
    )
    @app_commands.rename(user_to_ping='member')
    async def go_the_fuck_to_sleep(interaction: discord.Interaction, user_to_ping: discord.Member):
        current_user_id = interaction.user.id
        current_time = time.time()
        time_difference = current_time - (user_timestamps.get(current_user_id, {}).get("gothefucktosleep", 0))
        url = GO_THE_FUCK_TO_SLEEP_URLS[randint(0, len(GO_THE_FUCK_TO_SLEEP_URLS)-1)]
        if time_difference < COOLDOWN_DURATION:
            await interaction.response.send_message(
                f"<@{current_user_id}> {url} (cooldown: {round(COOLDOWN_DURATION - time_difference)}s)"
            )
            return

        await interaction.response.send_message(f"<@{user_to_ping.id}> {url}")

        log_event = {
            "event": "gothefucktosleep",
            "author_id": current_user_id,
            "mentioned_id": user_to_ping.id,
        }

        await logging.log_event(interaction, log_event, log_to_channel=False)
        user_timestamps.setdefault(current_user_id, {}).update({"gothefucktosleep": current_time})

    @tree.command(
        name="youhavetofuckingeat",
        description="You have to fucking eat",
        guilds=guilds,
    )
    async def you_have_to_fucking_eat(interaction: discord.Interaction, user_to_ping: discord.Member):
        current_user_id = interaction.user.id
        current_time = time.time()
        time_difference = current_time - (user_timestamps.get(current_user_id, {}).get("youhavetofuckingeat", 0))
        if time_difference < COOLDOWN_DURATION:
            await interaction.response.send_message(
                f"<@{current_user_id}> {YOU_HAVE_TO_FUCKING_EAT_URL} (cooldown: {round(COOLDOWN_DURATION - time_difference)}s)"
            )
            return

        await interaction.response.send_message(f"<@{user_to_ping.id}> {YOU_HAVE_TO_FUCKING_EAT_URL}")

        log_event = {
            "event": "youhavetofuckingeat",
            "author_id": current_user_id,
            "mentioned_id": user_to_ping.id,
        }

        await logging.log_event(interaction, log_event, log_to_channel=False)
        user_timestamps.setdefault(current_user_id, {}).update({"youhavetofuckingeat": current_time})

    @tree.command(
        name="youhavetofuckingeat_mika",
        description="Mika, go fucking eat",
        guilds=guilds,
    )
    async def fucking_eat_mika(interaction: discord.Interaction, user_to_ping: discord.Member = None):
        file = discord.File(MIKA_FUCKING_EAT_DIR)
        await interaction.response.send_message(f"<@{user_to_ping.id}>", file=file)
