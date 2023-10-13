import os
import shortuuid
from dotenv import load_dotenv
import discord
from ..modules import logging

load_dotenv()

TW_SERVER_CONFESSIONS_CHANNEL_ID = os.getenv(
    "TW_SERVER_CONFESSIONS_CHANNEL_ID")
BALTICS_SERVER_CONFESSIONS_CHANNEL_ID = os.getenv(
    "BALTICS_SERVER_CONFESSIONS_CHANNEL_ID")
TW_SERVER_CONFESSIONS_CHANNEL_OBJ = discord.Object(
    id=TW_SERVER_CONFESSIONS_CHANNEL_ID
)
BALTICS_SERVER_CONFESSIONS_CHANNEL_OBJ = discord.Object(
    id=BALTICS_SERVER_CONFESSIONS_CHANNEL_ID
)


def register_commands(
    tree: discord.app_commands.CommandTree,
    client: discord.Client,
    guilds: list,
):
    @tree.command(
        name="confess",
        description="Make an anonymous confession",
        guilds=[  # TW and Baltics server
            discord.Object(id=guilds[0]),
            discord.Object(id=guilds[1]),
        ],
    )
    async def confess(interaction: discord.Interaction, confession: str):
        """Write an anonymous confession.

        Args:
            interaction (discord.Interaction): required by discord.py
            confession (str): The confession to make.
        """
        server = (
            "TW" if (interaction.guild_id == int(guilds[0])) else "BALTICS"
        )
        confession_channel_id = int(
            TW_SERVER_CONFESSIONS_CHANNEL_ID
            if server == "TW"
            else BALTICS_SERVER_CONFESSIONS_CHANNEL_ID
        )
        confession_channel = client.get_channel(confession_channel_id)

        # Building the confession
        confession_id = shortuuid.uuid()
        embed = discord.Embed(title="Confession", description=confession)
        embed.set_footer(text=f"confession id: {confession_id}")
        confession_message = await confession_channel.send(embed=embed)

        log_event = {
            "event": "Confession",
            "user_id": f"<@{interaction.user.id}>",
            "server": server,
            "url": confession_message.jump_url,
            "id": confession_id,
        }

        await logging.log(f"[{confession_id}] {server} - {interaction.user.name} ({interaction.user.id}): {confession}", log_event)
        await interaction.response.send_message(
            f"Your confession has been sent to <#{confession_channel_id}>.",
            ephemeral=True,
        )
