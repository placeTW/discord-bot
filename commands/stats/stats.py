import discord
from discord import app_commands

from bot import TWPlaceClient
from commands.stats.stats_functions import get_pat_stats
from ..modules.supabase import supabaseClient


def register_commands(
    tree: discord.app_commands.CommandTree,
    client: TWPlaceClient,
    guilds: list[discord.Object],
):
    stats = app_commands.Group(name="stats", description="Stats functions")

    pat_stats = app_commands.Group(name="pat",description="Pat stats")

    @pat_stats.command(name='patted', description="Total patted stats")
    async def patted_stats(interaction: discord.Interaction):
        embed = get_pat_stats('patted')
        if embed is None:
            await interaction.response.send_message(
                f"There was an error getting the patted stats. Please try again",
                ephemeral=True,
            )
            return

        await interaction.response.send_message(embed=embed)
        

    @pat_stats.command(name='patter', description="Total patter stats")
    async def patted_stats(interaction: discord.Interaction):
        embed = get_pat_stats('patter')
        if embed is None:
            await interaction.response.send_message(
                f"There was an error getting the patter stats. Please try again",
                ephemeral=True,
            )
            return

        await interaction.response.send_message(embed=embed)

    stats.add_command(pat_stats)
    tree.add_command(stats, guilds=guilds)