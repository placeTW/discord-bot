
from discord import app_commands
from discord.app_commands import Choice

import discord
from commands.config.consts import POSSIBLE_CHANNEL_CONFIG_FIELDS
from commands.modules.supabase import supabaseClient

def set_server_config(guild_id: int, key: str, value: str, is_prod: bool):
    supabaseClient.table("server_config").update({key: value}).eq("guild_id", guild_id).eq("prod_config", is_prod).execute()

def register_commands(
    tree: discord.app_commands.CommandTree,
    guilds: list[discord.Object],
    is_prod: bool,
):
    config_group = app_commands.Group(name="config", description="Config functions")

    @config_group.command(
        name="channel",
        description="Sets a config value for a channel",
    )
    @app_commands.default_permissions(manage_guild=True)
    @app_commands.choices(channel_config=POSSIBLE_CHANNEL_CONFIG_FIELDS)
    @app_commands.describe(channel="The channel to set the config value for (defaults to current channel)")
    async def set_channel(interaction: discord.Interaction, channel_config: Choice[str], channel: discord.TextChannel = None):
        config_value = str(channel.id) if channel else interaction.channel_id
        set_server_config(interaction.guild_id, channel_config.value, config_value, is_prod)
        await interaction.response.send_message(f"Set {channel_config.name} to <#{config_value}> for this server {'(in dev config)' if not is_prod else ''}")

    tree.add_command(config_group, guilds=guilds)