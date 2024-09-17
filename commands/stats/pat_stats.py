import discord
from discord import app_commands
from modules.supabase import supabaseClient


def get_pat_stats(pat_type: str):
    data, c = supabaseClient.table(f'total_{pat_type}_counts').select("*").limit(10).execute()
    if c == 0:
        return None

    top_patted_users = data[1]
    embed = discord.Embed(title=f"Top 10 {pat_type}", color=discord.Color.blue())
    embed.description = '\n'.join(
        [f"{i+1}. <@{user_data['id']}>: {user_data['count']}" for i, user_data in enumerate(top_patted_users)]
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
