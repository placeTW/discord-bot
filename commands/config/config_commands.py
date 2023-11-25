
from discord import app_commands
from discord.app_commands import Choice
from commands.modules import logging

import discord
from bot import TWPlaceClient
from commands.config.consts import POSSIBLE_CHANNEL_CONFIG_FIELDS
from commands.modules.supabase import supabaseClient
from commands.modules.config import set_config

def register_commands(
    tree: discord.app_commands.CommandTree,
    client: TWPlaceClient,
    guilds: list[discord.Object],
):
    config_group = app_commands.Group(name="config", description="Config functions")

    @config_group.command(
        name="channel",
        description="Sets a config value for a channel",
    )
    @app_commands.default_permissions(manage_guild=True)
    @app_commands.choices(channel_config=POSSIBLE_CHANNEL_CONFIG_FIELDS)
    @app_commands.describe(channel="The channel to set the config value for (defaults to current channel) (requires manage server permissions)")
    async def set_channel(interaction: discord.Interaction, channel_config: Choice[str], channel: discord.TextChannel = None):
        if not interaction.permissions.manage_guild:
            await interaction.response.send_message(
                "You do not have the required permissions to use this command.", ephemeral=True
            )
            return
        config_value = str(channel.id) if channel else interaction.channel_id
        set_config(interaction.guild_id, channel_config.value, config_value, client.is_prod)
        client.fetch_config()
        log_event = {
            "event": "config channel",
            "author_id": interaction.user.id,
        }
        await logging.log_event(
            interaction,
            log_event,
            f"Set {channel_config.name} to <#{config_value}> for this server {'(in dev config)' if not client.is_prod else ''}",
        )
        await interaction.response.send_message(f"Set {channel_config.name} to <#{config_value}> for this server {'(in dev config)' if not client.is_prod else ''}", ephemeral=True)

    tree.add_command(config_group, guilds=guilds)

    @config_group.command(
        name="update",
        description="Updates the config from the database",
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def update_config(interaction: discord.Interaction):
        if not interaction.permissions.administrator:
            await interaction.response.send_message(
                "You do not have the required permissions to use this command.", ephemeral=True
            )
            return
        client.fetch_config()
        await interaction.response.send_message(f"Config updated from database {'(in dev config)' if not client.is_prod else ''}", ephemeral=True)