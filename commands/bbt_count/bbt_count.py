import datetime
import discord
from discord import app_commands
from babel import numbers


from bot import TWPlaceClient

from .db_functions import (
    add_bbt_entry,
    remove_bbt_entry,
    get_bbt_entry,
    edit_bbt_entry,
    get_bbt_entries,
    get_bbt_leaderboard,
)
from .helpers import (
    bubble_tea_string,
    calculate_prices,
    bbt_embed,
)
from ..modules import logging, content_moderation


def register_commands(
    tree: discord.app_commands.CommandTree,
    client: TWPlaceClient,
    guilds: list[discord.Object],
):
    bbt_count = app_commands.Group(
        name="bbt_count", description="Bubble tea counts"
    )

    # add
    @bbt_count.command(name="add", description="Add a new bubble tea entry")
    @app_commands.describe(
        description="Short description of the bubble tea that you got"
    )
    @app_commands.describe(
        location="Where you got the bubble tea from (optional)"
    )
    @app_commands.describe(
        image="Image of the bubble tea (optional, not saved in database)"
    )
    @app_commands.describe(price="Price of the bubble tea (optional)")
    @app_commands.describe(
        currency="Currency of the price (optional, Taiwan dollar = TWD, US dollar = USD, etc.)"
    )
    async def bbt_count_add(
        interaction: discord.Interaction,
        description: str,
        location: str = None,
        image: discord.Attachment = None,
        price: float = None,
        currency: str = None,
    ):
        await interaction.response.defer()
        if image and not (
            await content_moderation.review_image(image)
            or not image.content_type.startswith("image/")
        ):
            await interaction.followup.send(
                "Image rejected by content moderation.",
                ephemeral=True,
            )
            return

        add_data = {}
        if description:
            add_data["description"] = description
        if location:
            add_data["location"] = location
        if image:
            add_data["image"] = image.url
        if price:
            add_data["price"] = price
        if currency:
            add_data["currency"] = currency

        id = add_bbt_entry(
            interaction.created_at,
            interaction.user.id,
            interaction.guild.id,
            **add_data,
        )

        log_event = {
            "event": "Bubble tea entry",
            "author_id": interaction.user.id,
            "generated_id": str(id),
            "metadata": {
                "description": description,
                "location": location if location else None,
                "image": image.url if image else None,
                "price": price if price else None,
                "currency": currency if currency else None,
            },
        }
        await logging.log_event(
            interaction, log_event, content=description, log_to_channel=False
        )

        embed = bbt_embed(
            id,
            interaction.user.id,
            str(interaction.created_at.date()),
            interaction.user.display_name,
            interaction.user.avatar.url,
            add_data,
            new=True,
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

        embed = bbt_embed(
            id,
            None,
            None,
            interaction.user.display_name,
            interaction.user.avatar.url,
            entry,
        )
        await interaction.response.send_message(embed=embed)

    # edit
    @bbt_count.command(name="edit", description="Edit a bubble tea entry")
    @app_commands.describe(id="ID of the bubble tea entry to edit")
    @app_commands.describe(
        description="Short description of the bubble tea that you got (optional)"
    )
    @app_commands.describe(
        location="Where you got the bubble tea from (optional)"
    )
    @app_commands.describe(
        image="Image of the bubble tea (optional, not saved in database)"
    )
    @app_commands.describe(price="Price of the bubble tea (optional)")
    @app_commands.describe(currency="Currency of the price (optional)")
    async def bbt_count_edit(
        interaction: discord.Interaction,
        id: int,
        description: str = None,
        location: str = None,
        image: discord.Attachment = None,
        price: float = None,
        currency: str = None,
    ):
        await interaction.response.defer()
        if image and not await content_moderation.review_image(image):
            await interaction.followup.send(
                "Image rejected by content moderation.",
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

        edit_data = {}
        if description:
            edit_data["description"] = description
        if location:
            edit_data["location"] = location
        if image:
            edit_data["image"] = image.url
        if price:
            edit_data["price"] = price
        if currency:
            edit_data["currency"] = currency

        edit_bbt_entry(id, interaction.user.id, **edit_data)

        log_event = {
            "event": "Bubble tea entry edit",
            "author_id": interaction.user.id,
            "generated_id": str(id),
            "metadata": {
                "description": description
                if description
                else entry["description"],
                "location": location if location else entry["location"],
                "image": image.url if image else entry["image"],
                "price": price if price else entry["price"],
                "currency": currency if currency else entry["currency"],
            },
        }
        await logging.log_event(
            interaction,
            log_event,
            content=description if description else entry["description"],
            log_to_channel=False,
        )

        embed = bbt_embed(
            id,
            interaction.user.id,
            None,
            interaction.user.display_name,
            interaction.user.avatar.url,
            {**entry, **edit_data},
        )
        await interaction.followup.send(embed=embed)

    # list
    @bbt_count.command(
        name="list",
        description="List the bubble tea entries for a user in a given year",
    )
    @app_commands.describe(
        user="User to list entries for (optional, default to self)"
    )
    @app_commands.describe(
        year="Year to list entries for (optional, default to current year)"
    )
    async def bbt_count_list(
        interaction: discord.Interaction,
        user: discord.User = None,
        year: int = None,
    ):
        await interaction.response.defer()
        entries = get_bbt_entries(
            user.id if user else interaction.user.id, year
        )
        prices = calculate_prices(entries)
        embed = discord.Embed(
            title=f"Bubble tea entries {f'for {year}' if year else 'for the past year'} 🧋",
            color=discord.Color.blue(),
        )
        embed.description = (
            f"For <@{user.id if user else interaction.user.id}>: **{len(entries)} total entries**"
            + "\n\nTotal costs: "
            + " + ".join(
                [
                    f"{numbers.format_currency(prices[currency]['total'], currency, locale='en_US')} ({prices[currency]['count']}, avg {numbers.format_currency(prices[currency]['total']/prices[currency]['count'], currency, locale='en_US')}/🧋)"
                    for currency in prices
                ]
            )
            + "\n\n"
            + "\n".join(
                [
                    f"`{entry['id']}: {str(datetime.datetime.fromisoformat(entry['created_at']).date())}` - {bubble_tea_string(entry['description'], entry['location'], entry['price'], entry['currency'])}{' (no image)' if not entry['image'] else ''}"
                    for entry in entries
                ]
            )
        )
        await interaction.followup.send(embed=embed)

    # leaderboard
    @bbt_count.command(
        name="leaderboard",
        description="List the top bubble tea drinkers in a given year",
    )
    @app_commands.describe(
        year="Year to list leaderboard for (optional, default to current year)"
    )
    async def bbt_count_leaderboard(
        interaction: discord.Interaction, year: int = None
    ):
        await interaction.response.defer()
        leaderboard = get_bbt_leaderboard(
            interaction.guild.id,
            datetime.datetime(year=year, month=1, day=1)
            if year
            else interaction.created_at,
        )
        embed = discord.Embed(
            title=f"Top bubble tea drinkers of {year if year else interaction.created_at.year} in {client.guilds_dict[interaction.guild.id]['server_name']}",
            color=discord.Color.blue(),
        )
        embed.description = "\n".join(
            [
                f"{i+1}. <@{user_data['user_id']}>: {user_data['count']} 🧋"
                for i, user_data in enumerate(leaderboard)
            ]
        )
        await interaction.followup.send(embed=embed)

    tree.add_command(bbt_count, guilds=guilds)
