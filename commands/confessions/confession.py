import os
import shortuuid
import discord
from ..modules import logging


def register_commands(
    tree: discord.app_commands.CommandTree,
    client: discord.Client,
    guilds_dict: dict,
):
    @tree.command(
        name="confess",
        description="Make an anonymous confession",
        guilds=[  # TW and Baltics server
            discord.Object(id=int(server_id))
            for server_id, server_info in guilds_dict.items()
            if "CONFESSIONS_CHANNEL_ID" in server_info
        ],
    )
    async def confess(interaction: discord.Interaction, confession: str):
        """Write an anonymous confession.

        Args:
            interaction (discord.Interaction): required by discord.py
            confession (str): The confession to make.
        """

        # Getting the confession channel
        confession_channel_id = guilds_dict[str(interaction.guild.id)][
            "CONFESSIONS_CHANNEL_ID"
        ]
        confession_channel = client.get_channel(confession_channel_id)

        # Building the confession
        confession_id = shortuuid.uuid()
        embed = discord.Embed(title="Confession", description=confession)
        embed.set_footer(text=f"confession id: {confession_id}")
        confession_message = await confession_channel.send(embed=embed)
        confession_url = confession_message.jump_url

        log_event = {
            "event": "Confession",
            "user_id": f"<@{interaction.user.id}>",
            "server": interaction.guild.name,
            "url": confession_url,
            "id": confession_id,
        }

        await logging.log(
            f"[{confession_id}] {interaction.guild.name} - {interaction.user.name} ({interaction.user.id}): {confession}",
            log_event,
        )
        await interaction.response.send_message(
            f"Your confession has been sent. See it here: {confession_url}",
            ephemeral=True,
        )
