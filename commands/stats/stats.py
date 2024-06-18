import discord
from discord import app_commands

from bot import TWPlaceClient
from commands.stats.pat_stats import pat_stats_commands
from modules.supabase import supabaseClient


def register_commands(
    tree: discord.app_commands.CommandTree,
    client: TWPlaceClient,
    guilds: list[discord.Object],
):
    stats = app_commands.Group(name="stats", description="Stats functions")
    pat_stats = pat_stats_commands()

    stats.add_command(pat_stats)
    tree.add_command(stats, guilds=guilds)