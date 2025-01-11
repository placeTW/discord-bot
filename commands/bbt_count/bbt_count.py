import datetime
import discord
from discord import app_commands

from bot import TWPlaceClient
from commands.bbt_count.consts import BBT_LIST_GROUP_BY_CHOICES
from components.paginator import GenericPaginator

from .db_functions import (
    add_bbt_entry,
    get_bubble_tea_monthly_counts,
    remove_bbt_entry,
    get_bbt_entry,
    edit_bbt_entry,
    get_bbt_entries,
    get_bbt_leaderboard,
    get_bubble_tea_stats,
    get_latest_bubble_tea_entry,
)
from .embeds import (
    bbt_entry_embed,
    bbt_list_default_embed,
    bbt_list_grouped_embed,
    user_transfer_embed,
    bbt_stats_embed,
)
from .helpers import bubble_tea_data, calculate_prices
from modules import logging


def register_commands(
    tree: app_commands.CommandTree,
    client: TWPlaceClient,
    guilds: list[discord.Object],
):
    bbt_count = app_commands.Group(name="bbt_count", description="Bubble tea counts")

    # add
    @bbt_count.command(name="add", description="Add a new bubble tea entry")
    @app_commands.describe(description="Short description of the bubble tea that you got")
    @app_commands.describe(date="Date of the bubble tea (optional, must be in the format YYYY-MM-DD, e.g. 2021-12-31)")
    @app_commands.describe(location="Where you got the bubble tea from (optional)")
    @app_commands.describe(image="Image of the bubble tea (optional, not saved in database)")
    @app_commands.describe(price="Price of the bubble tea (optional)")
    @app_commands.describe(currency="Currency of the price (optional, Taiwan dollar = TWD, US dollar = USD, etc.)")
    @app_commands.describe(notes="Additional notes (optional)")
    @app_commands.describe(rating="Personal rating of the bubble tea (optional)")
    async def bbt_count_add(
        interaction: discord.Interaction,
        description: str,
        date: str = None,
        location: str = None,
        image: discord.Attachment = None,
        price: float = None,
        currency: str = None,
        notes: str = None,
        rating: float = None,
    ):
        await interaction.response.defer()

        if image and not image.content_type.startswith("image/"):
            await interaction.followup.send(
                "Invalid image type. Please upload an image file.",
                ephemeral=True,
            )
            return

        if date:
            try:
                created_at = datetime.datetime.fromisoformat(date).astimezone()
            except ValueError:
                await interaction.followup.send(
                    "Invalid date format. Please use the format YYYY-MM-DD, e.g. 2021-12-31",
                    ephemeral=True,
                )
                return

        add_data = bubble_tea_data(
            description,
            None,
            None,
            location,
            price,
            currency,
            image.url if image else None,
            notes,
            rating,
        )

        id = add_bbt_entry(
            created_at if date and created_at else interaction.created_at,
            interaction.user.id,
            interaction.guild.id,
            **add_data,
        )

        log_event = {
            "event": "Bubble tea entry",
            "author_id": interaction.user.id,
            "generated_id": str(id),
            "metadata": add_data,
        }
        await logging.log_event(interaction, log_event, content=description, log_to_channel=False)

        embed = bbt_entry_embed(
            id,
            interaction.user.id,
            str(created_at.date()) if date and created_at else str(interaction.created_at.date()),
            interaction.user.display_name,
            interaction.user.avatar.url,
            add_data,
            interaction.created_at.astimezone().tzinfo,
            title_prefix="New",
        )
        await interaction.followup.send(embed=embed)

    # remove
    @bbt_count.command(name="remove", description="Remove a bubble tea entry")
    @app_commands.describe(id="ID of the bubble tea entry to remove")
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

    # get
    @bbt_count.command(name="get", description="Get a bubble tea entry")
    @app_commands.describe(id="ID of the bubble tea entry to get")
    async def bbt_count_get(interaction: discord.Interaction, id: int):
        entry = get_bbt_entry(id)
        if not entry:
            await interaction.response.send_message(
                f"Entry {id} not found",
                ephemeral=True,
            )
            return

        embed = bbt_entry_embed(
            id,
            None,
            None,
            (interaction.user.display_name if interaction.user.id == entry.get("user_id") else None),
            (interaction.user.avatar.url if interaction.user.id == entry.get("user_id") else None),
            entry,
            interaction.created_at.astimezone().tzinfo,
        )
        await interaction.response.send_message(embed=embed)

    # edit
    @bbt_count.command(name="edit", description="Edit a bubble tea entry")
    @app_commands.describe(id="ID of the bubble tea entry to edit")
    @app_commands.describe(date="Date of the bubble tea (optional, must be in the format YYYY-MM-DD, e.g. 2021-12-31)")
    @app_commands.describe(description="Short description of the bubble tea that you got (optional)")
    @app_commands.describe(location="Where you got the bubble tea from (optional)")
    @app_commands.describe(image="Image of the bubble tea (optional, not saved in database)")
    @app_commands.describe(price="Price of the bubble tea (optional)")
    @app_commands.describe(currency="Currency of the price (optional)")
    @app_commands.describe(notes="Additional notes (optional)")
    @app_commands.describe(rating="Personal rating of the bubble tea (optional)")
    @app_commands.describe(transfer_user="Transfer the entry to another user (optional)")
    async def bbt_count_edit(
        interaction: discord.Interaction,
        id: int,
        date: str = None,
        description: str = None,
        transfer_user: discord.User = None,
        location: str = None,
        image: discord.Attachment = None,
        price: float = None,
        currency: str = None,
        notes: str = None,
        rating: float = None,
    ):
        await interaction.response.defer()
        if image and not image.content_type.startswith("image/"):
            await interaction.followup.send(
                "Invalid image type. Please upload an image file.",
                ephemeral=True,
            )
            return

        if date:
            try:
                created_at = datetime.datetime.fromisoformat(date).astimezone()
            except ValueError:
                await interaction.followup.send(
                    "Invalid date format. Please use the format YYYY-MM-DD, e.g. 2021-12-31",
                    ephemeral=True,
                )
                return

        entry = get_bbt_entry(id)
        if not entry:
            await interaction.followup.send(
                f"Entry {id} not found",
                ephemeral=True,
            )
            return

        if entry["user_id"] != interaction.user.id:
            await interaction.followup.send(
                f"Entry {id} does not belong to you",
                ephemeral=True,
            )
            return

        async def edit(user: discord.User = None):
            edit_data = bubble_tea_data(
                description,
                user.id if user else None,
                str(created_at) if date and created_at else None,
                location,
                price,
                currency,
                image.url if image else None,
                notes,
                rating,
            )

            edit_bbt_entry(id, interaction.user.id, **edit_data)

            log_event = {
                "event": "Bubble tea entry edit",
                "author_id": interaction.user.id,
                "generated_id": str(id),
                "metadata": {**entry, **edit_data},
            }
            await logging.log_event(
                interaction,
                log_event,
                content=description if description else entry["description"],
                log_to_channel=False,
            )

            embed = bbt_entry_embed(
                id,
                interaction.user.id,
                None,
                interaction.user.display_name,
                interaction.user.avatar.url,
                {**entry, **edit_data},
                interaction.created_at.astimezone().tzinfo,
                title_prefix="Edited",
            )
            await interaction.followup.send(embed=embed)

        # Show transfer button choices if transfer_user is specified
        if transfer_user and transfer_user.id != interaction.user.id:

            class TransferButtonView(discord.ui.View):
                def __init__(self):
                    super().__init__()
                    self.msg: discord.Message = None

                @discord.ui.button(label="Yes", style=discord.ButtonStyle.green)
                async def transfer_button_yes(
                    self,
                    interaction: discord.Interaction,
                    button: discord.ui.Button,
                ):
                    await self.msg.edit(
                        content=f"Transferring entry #{id} to <@{transfer_user.id}>",
                        embed=None,
                        view=None,
                    )
                    # Transfer the entry to the new user
                    await edit(transfer_user)

                @discord.ui.button(label="No", style=discord.ButtonStyle.red)
                async def transfer_button_no(
                    self,
                    interaction: discord.Interaction,
                    button: discord.ui.Button,
                ):
                    await self.msg.edit(content="Transfer cancelled", embed=None, view=None)
                    # Cancel the transfer and edit the entry normally
                    await edit()

            button = TransferButtonView()
            msg: discord.Message = await interaction.followup.send(
                embed=user_transfer_embed(transfer_user.id, id),
                view=button,
            )
            button.msg = msg
            return
        # Otherwise normally edit the entry
        else:
            await edit()

    # list
    @bbt_count.command(
        name="list",
        description="List the bubble tea entries for a user in a given year",
    )
    @app_commands.describe(user="User to list entries for (optional, default to self)")
    @app_commands.describe(year="Year to list entries for (optional, default to current year)")
    @app_commands.describe(group_by="Field to group by (optional)")
    @app_commands.choices(group_by=BBT_LIST_GROUP_BY_CHOICES)
    async def bbt_count_list(
        interaction: discord.Interaction,
        user: discord.User = None,
        year: int = None,
        group_by: app_commands.Choice[str] = None,
    ):
        await interaction.response.defer()
        entries = get_bbt_entries(user.id if user else interaction.user.id, year)
        
        if not entries:
            embed = discord.Embed(
                title="No bubble tea entries found",
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=embed)
            return

        total_prices = calculate_prices(entries, None)["default_group"]
        
        if group_by:
            embeds = bbt_list_grouped_embed(
                user.id if user else interaction.user.id,
                entries,
                year,
                interaction.created_at.astimezone().tzinfo,
                group_by.value,
                total_prices,
            )
        else:
            embeds = bbt_list_default_embed(
                user.id if user else interaction.user.id,
                entries,
                year,
                interaction.created_at.astimezone().tzinfo,
                total_prices,
                len(entries),
            )

        paginator = GenericPaginator(embeds)
        await interaction.followup.send(embed=embeds[0], view=paginator)

    # leaderboard
    @bbt_count.command(
        name="leaderboard",
        description="List the top bubble tea drinkers in a given year",
    )
    @app_commands.describe(year="Year to list leaderboard for (optional, default to current year)")
    async def bbt_count_leaderboard(interaction: discord.Interaction, year: int = None):
        await interaction.response.defer()
        leaderboard = get_bbt_leaderboard(
            interaction.guild.id,
            (datetime.datetime(year=year, month=1, day=1) if year else interaction.created_at),
        )
        
        if not leaderboard:
            embed = discord.Embed(
                title="No leaderboard data found",
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=embed)
            return

        # Split into chunks of 10 entries per page
        chunks = [leaderboard[i:i + 10] for i in range(0, len(leaderboard), 10)]
        embeds = []
        
        for i, chunk in enumerate(chunks):
            embed = discord.Embed(
                title=f"Top bubble tea drinkers of {year if year else interaction.created_at.year} in {client.guilds_dict[interaction.guild.id]['server_name']}",
                color=discord.Color.blue(),
            )
            embed.description = "\n".join(
                [
                    f"{j + (i*10) + 1}. <@{user_data.get('user_id')}>: {user_data.get('count')} 🧋"
                    + (
                        f" *average given rating: {user_data.get('average_rating'):.3f}*"
                        if user_data.get("average_rating")
                        else ""
                    )
                    for j, user_data in enumerate(chunk)
                ]
            )
            embed.set_footer(text=f"Page {i+1} of {len(chunks)} • Total entries: {len(leaderboard)}")
            embeds.append(embed)

        paginator = GenericPaginator(embeds)
        await interaction.followup.send(embed=embeds[0], view=paginator)


    @bbt_count.command(name="stats", description="Get the stats for a user for a given year")
    @app_commands.describe(user="User to get stats for (optional, default to self)")
    @app_commands.describe(year="Year to get stats for (optional, default to current year)")
    @app_commands.describe(group_by_location="Group the stats by location (optional)")
    async def bbt_count_stats(
        interaction: discord.Interaction,
        user: discord.User = None,
        year: int = None,
        group_by_location: bool = False,
    ):
        await interaction.response.defer()
        user_id = user.id if user else interaction.user.id
        stats = get_bubble_tea_stats(
            user_id,
            (datetime.datetime(year=year, month=1, day=1) if year else interaction.created_at),
            group_by_location,
        )
        monthly_counts = get_bubble_tea_monthly_counts(
            user_id,
            (datetime.datetime(year=year, month=1, day=1) if year else interaction.created_at),
        )

        latest = (
            get_latest_bubble_tea_entry(user_id)
            if not year or (year and year == datetime.datetime.now().year)
            else None
        )

        if group_by_location and stats.get('location_stats'):
            # Split location stats into chunks of 10
            location_stats = list(stats['location_stats'].items())
            chunks = [location_stats[i:i + 10] for i in range(0, len(location_stats), 10)]
            embeds = []

            for i, chunk in enumerate(chunks):
                embed = bbt_stats_embed(
                    user_id,
                    {**stats, 'location_stats': dict(chunk)},
                    year,
                    group_by_location,
                    monthly_counts if i == 0 else None,  # Only show monthly counts on first page
                    latest if i == 0 else None,  # Only show latest on first page
                    interaction.created_at.astimezone().tzinfo,
                )
                embed.set_footer(text=f"Page {i+1} of {len(chunks)} • Total locations: {len(location_stats)}")
                embeds.append(embed)

            paginator = GenericPaginator(embeds)
            await interaction.followup.send(embed=embeds[0], view=paginator)
        else:
            embed = bbt_stats_embed(
                user_id,
                stats,
                year,
                group_by_location,
                monthly_counts,
                latest,
                interaction.created_at.astimezone().tzinfo,
            )
            await interaction.followup.send(embed=embed)


    tree.add_command(bbt_count, guilds=guilds)
