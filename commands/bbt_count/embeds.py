import discord
import datetime
import calendar

from commands.bbt_count.helpers import (
    bubble_tea_string,
    calculate_prices,
    entry_string,
    price_string,
    cost_string_prices,
    cost_string,
    average_year_string,
    average_month_string,
)


def bbt_entry_embed(
    id: int,
    user_id: int,
    date: str,
    name: str | None,
    icon_url: str | None,
    entry: dict,
    timezone: datetime.tzinfo,
    title_prefix="",
):
    embed = discord.Embed(
        title=f"{title_prefix} Bubble tea entry #{id}".strip(),
        description=f"Entry #{id} from <@{entry.get('user_id', user_id)}>: {bubble_tea_string(entry.get('description'), entry.get('location'), entry.get('price'), entry.get('currency'))}",
        color=discord.Color.green(),
    )
    if name and icon_url:
        embed.set_author(name=name, icon_url=icon_url)
    if entry.get("image"):
        embed.set_image(url=entry.get("image"))
    embed.add_field(
        name="Date",
        value=(
            date
            if date
            else str(
                datetime.datetime.fromisoformat(entry.get("created_at"))
                .astimezone(timezone)
                .date()
            )
        ),
        inline=False,
    )
    embed.add_field(
        name="Description", value=entry.get("description"), inline=False
    )
    embed.add_field(name="Location", value=entry.get("location"), inline=False)
    embed.add_field(
        name="Price",
        value=price_string(entry.get("price"), entry.get("currency")),
        inline=False,
    )
    if entry.get("notes"):
        embed.add_field(name="Notes", value=entry.get("notes"), inline=False)
    if entry.get("rating"):
        embed.add_field(name="Rating", value=entry.get("rating"), inline=False)
    embed.set_footer(text=f"id: {id}")

    return embed


def user_transfer_embed(
    transfer_user_id: int,
    entry_id: int,
):
    embed = discord.Embed(
        title=f"Transferring entry #{entry_id} 🧋",
        description=f"Are you sure you want to transfer this bubble tea entry to <@{transfer_user_id}>?\n\n**This action is irreversible**",
        color=discord.Color.red(),
    )
    return embed


def bbt_list_default_embed(
    user_id: int,
    entries: list[dict],
    year: int | None,
    timezone: datetime.tzinfo,
):
    prices = calculate_prices(entries, None).get("default_group", {})
    embed = discord.Embed(
        title=f"Bubble tea entries {f'for {year}' if year else 'for the past year'} 🧋",
        color=discord.Color.blue(),
    )
    embed.description = (
        f"For <@{user_id}>: **{len(entries)} total entries**\n{average_year_string(year, len(entries))}"
        + (
            "\n\n__Total costs__:\n"
            + "\n".join(
                [
                    cost_string_prices(prices[currency]["prices"], currency)
                    for currency in prices
                ]
            )
            + "\n\n"
            + "\n".join([entry_string(entry, timezone) for entry in entries])
        )
        if len(entries)
        else ""
    )
    return embed


def bbt_list_grouped_embed(
    user_id: int,
    entries: list[dict],
    year: int,
    timezone: datetime.tzinfo,
    group_by: str,
):
    prices = calculate_prices(entries, group_by)
    embed = discord.Embed(
        title=f"Bubble tea entries {f'for {year}' if year else 'for the past year'} grouped by {group_by} 🧋",
        color=discord.Color.blue(),
    )
    embed.description = f"For <@{user_id}>: **{len(entries)} total entries**"

    for group in prices:
        group_entries = [
            entry for entry in entries if entry[group_by] == group
        ]
        embed.description += (
            f"\n\n---\n**{group}: {len(group_entries)} entries**"
        )
        for currency in prices[group]:
            embed.description += f"\n{currency}: {cost_string_prices(prices[group][currency]['prices'], currency)}"
        embed.description += "\n\n"
        embed.description += "\n".join(
            [entry_string(entry, timezone) for entry in group_entries]
        )
    return embed


def bbt_stats_embed(
    user_id: int,
    entries: list[dict],
    year: int,
    group_by_location: bool,
    monthly_counts: list[dict],
    latest: dict,
    timezone: datetime.tzinfo,
):
    total_count = sum([entry.get("entry_count", 0) for entry in entries])
    embed = discord.Embed(
        title=f"Bubble tea stats {f'for {year}' if year else 'for the past year'} {'grouped by location ' if group_by_location else ''}🧋",
        color=discord.Color.green(),
    )
    embed.description = f"For <@{user_id}>: **{total_count} total entries**\n{average_year_string(year, total_count)}\n\n"
    if total_count > 0:
        embed.description += f"{'__Total costs__' if not group_by_location else '__Costs by location__'}:\n"
        embed.description += "\n".join(
            [
                (
                    "- "
                    + (
                        f'**{entry.get("location")}**: '
                        if group_by_location
                        else ""
                    )
                    + cost_string(
                        entry.get("total_price") or 0,
                        entry.get("entry_count", 0),
                        entry.get("currency"),
                    )
                    + (
                        f" *average given rating: {entry.get('average_rating'):.3f}*"
                        if entry.get("average_rating")
                        else ""
                    )
                )
                for entry in entries
            ]
        )
        current_year = year if year else datetime.datetime.now().year
        embed.description += "\n\n__Monthly counts__:\n"
        embed.description += "\n".join(
            [
                f"**{calendar.month_name[monthly_count.get('month', 0)]}**: {monthly_count.get('entry_count')} entries ({average_month_string(current_year, monthly_count.get('month', 0), monthly_count.get('entry_count'))})"
                + (
                    f"\n- *average given rating: {monthly_count.get('average_rating'):.3f}*"
                    if monthly_count.get("average_rating")
                    else ""
                )
                for monthly_count in monthly_counts
            ]
        )
        if latest:
            embed.description += "\n\n**Latest entry**:\n"
            embed.description += entry_string(latest, timezone)
    return embed
