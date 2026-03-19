import discord
from discord import app_commands
from psycopg2 import sql

from modules.db import get_cursor

_ALLOWED_PAT_TYPES = frozenset({"patted", "patter"})


def get_pat_stats(pat_type: str):
    if pat_type not in _ALLOWED_PAT_TYPES:
        raise ValueError(f"Invalid pat_type: {pat_type}")
    with get_cursor() as cur:
        cur.execute(
            sql.SQL("SELECT id, count FROM {} LIMIT 10").format(
                sql.Identifier(f"total_{pat_type}_counts")
            )
        )
        rows = cur.fetchall()
    if not rows:
        return None

    embed = discord.Embed(title=f"Top 10 {pat_type}", color=discord.Color.blue())
    embed.description = '\n'.join(
        [f"{i+1}. <@{row['id']}>: {row['count']}" for i, row in enumerate(rows)]
    )
    return embed


def pat_stats_commands():
    pat_stats = app_commands.Group(name="pat", description="Pat stats")

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

    return pat_stats
