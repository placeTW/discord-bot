import datetime
import discord
from discord import app_commands

from bot import TWPlaceClient

from .db_functions import add_bbt_entry, remove_bbt_entry, get_bbt_entries, get_bbt_leaderboard
from ..modules import content_moderation


def bubble_tea_string(description: str, location: str):
    return f"{description}{f' at {location}' if location else ''}"


def register_commands(
    tree: discord.app_commands.CommandTree,
    client: TWPlaceClient,
    guilds: list[discord.Object],
):
    bbt_count = app_commands.Group(
        name="bbt_count", description="Bubble tea counts")

    # add
    @bbt_count.command(name='add', description="Add a new bubble tea entry")
    @app_commands.describe(description="Short description of the bubble tea that you got")
    @app_commands.describe(location="Where you got the bubble tea from (optional)")
    @app_commands.describe(image="Image of the bubble tea (optional, not saved in database)")
    async def bbt_count_add(interaction: discord.Interaction, description: str, location: str = None, image: discord.Attachment = None):
        await interaction.response.defer()
        id = add_bbt_entry(interaction.created_at, interaction.user.id,
                           interaction.guild.id, location, description)
        embed = discord.Embed(
            title="New bubble tea entry",
            description=f"<@{interaction.user.id}> added a bubble tea entry: {bubble_tea_string(description, location)} 🧋",
            color=discord.Color.green(),
        )
        embed.set_author(name=interaction.user.display_name,
                         icon_url=interaction.user.avatar.url)
        embed.add_field(name="Description", value=description, inline=False)
        embed.add_field(name="Location", value=location, inline=False)
        embed.set_footer(text=f"id: {id}")

        if image and image.content_type.startswith('image/') and await content_moderation.review_image(image):
            embed.set_image(url=image.url)

        await interaction.followup.send(embed=embed)

    # remove
    @bbt_count.command(name='remove', description="Remove a bubble tea entry")
    async def bbt_count_remove(interaction: discord.Interaction, id: int):
        try:
            remove_bbt_entry(id, interaction.user.id)
            await interaction.response.send_message(
                f"Removed entry {id}",
                ephemeral=True,
            )
        except:
            await interaction.response.send_message(
                f"Failed to remove {id}",
                ephemeral=True,
            )

    # list
    @bbt_count.command(name='list', description="list bbt_count")
    @app_commands.describe(user="User to list entries for (optional, default to self)")
    @app_commands.describe(year="Year to list entries for (optional, default to current year)")
    async def bbt_count_list(interaction: discord.Interaction, user: discord.User = None, year: int = None):
        await interaction.response.defer()
        entries = get_bbt_entries(
            user.id if user else interaction.user.id, year)
        embed = discord.Embed(
            title=f"Bubble tea entries {f'for {year}' if year else 'for the past year'} 🧋", color=discord.Color.blue())
        embed.description = f'For <@{user.id if user else interaction.user.id}>: {len(entries)} entries\n\n' + '\n'.join(
            [f"{entry['id']}. {str(datetime.datetime.fromisoformat(entry['created_at']).date())} - {bubble_tea_string(entry['description'], entry['location'])}" for entry in entries])
        await interaction.followup.send(embed=embed)

    # leaderboard
    @bbt_count.command(name='leaderboard', description="leaderboard bbt_count")
    @app_commands.describe(year="Year to list leaderboard for (optional, default to current year)")
    async def bbt_count_leaderboard(interaction: discord.Interaction, year: int = None):
        await interaction.response.defer()
        leaderboard = get_bbt_leaderboard(interaction.guild.id, datetime.datetime(
            year=year, month=1, day=1) if year else interaction.created_at)
        embed = discord.Embed(
            title=f"Top bubble tea drinkers of {year if year else interaction.created_at.year} in {client.guilds_dict[interaction.guild.id]['server_name']}", color=discord.Color.blue())
        embed.description = '\n'.join(
            [f"{i+1}. <@{user_data['user_id']}>: {user_data['count']} 🧋" for i, user_data in enumerate(leaderboard)])
        await interaction.followup.send(embed=embed)

    tree.add_command(bbt_count, guilds=guilds)
