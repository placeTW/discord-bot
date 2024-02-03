import discord
import datetime

from commands.bbt_count.helpers import (
    bubble_tea_string,
    calculate_prices,
    entry_string,
    price_string,
    cost_string,
)


def bbt_entry_embed(
    id: int,
    user_id: int,
    date: str,
    name: str,
    icon_url: str,
    entry: dict,
    title_prefix="",
):
    embed = discord.Embed(
        title=f"{title_prefix} Bubble tea entry #{id}".strip(),
        description=f"Entry #{id} from <@{entry.get('user_id', user_id)}>: {bubble_tea_string(entry.get('description'), entry.get('location'), entry.get('price'), entry.get('currency'))}",
        color=discord.Color.green(),
    )
    embed.set_author(
        name=name,
        icon_url=icon_url,
    )
    if entry.get("image"):
        embed.set_image(url=entry.get("image"))
    embed.add_field(
        name="Date",
        value=date
        if date
        else str(
            datetime.datetime.fromisoformat(entry.get("created_at")).date()
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
    embed.set_footer(text=f"id: {id}")

    return embed


def bbt_list_default_embed(
    user_id: int,
    entries: list[dict],
    year: int,
):
    prices = calculate_prices(entries, None).get("default_group", {})
    embed = discord.Embed(
        title=f"Bubble tea entries {f'for {year}' if year else 'for the past year'} 🧋",
        color=discord.Color.blue(),
    )
    embed.description = (
        f"For <@{user_id}>: **{len(entries)} total entries**"
        + "\n\n__Total costs__:\n"
        + "\n".join(
            [
                cost_string(prices[currency]["prices"], currency)
                for currency in prices
            ]
        )
        + "\n\n"
        + "\n".join([entry_string(entry) for entry in entries])
    )
    return embed


def bbt_list_grouped_embed(
    user_id: int,
    entries: list[dict],
    year: int,
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
            embed.description += f"\n{currency}: {cost_string(prices[group][currency]['prices'], currency)}"
        embed.description += "\n\n"
        embed.description += "\n".join(
            [entry_string(entry) for entry in group_entries]
        )
    return embed
