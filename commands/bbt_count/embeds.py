import discord
import datetime
import calendar

from commands.bbt_count.helpers import (
    bubble_tea_string,
    calculate_prices,
    entry_string,
    organize_entries_by_group,
    price_string,
    cost_string,
    average_year_string,
    average_month_string,
    rating_string,
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
            str(datetime.datetime.fromisoformat(entry.get("created_at")).astimezone(timezone).date())
            if entry.get("created_at")
            else date
        ),
        inline=False,
    )
    embed.add_field(name="Description", value=entry.get("description"), inline=False)
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
    total_prices: dict = None,
    total_entries: int = 0,
    items_per_page: int = 10,
):
    chunks = [entries[i:i + items_per_page] for i in range(0, len(entries), items_per_page)]
    embeds = []
    
    for i, chunk in enumerate(chunks):
        prices = calculate_prices(chunk, None).get("default_group", {})
        
        embed = discord.Embed(
            title=f"Bubble tea entries {f'for {year}' if year else 'for the past year'} 🧋",
            color=discord.Color.blue(),
        )
        embed.description = (
            f"For <@{user_id}>: **{total_entries} total entries**\n{average_year_string(year, total_entries)}"
            + (
                "\n\n__Total costs (all entries)__:\n"
                + "\n".join([cost_string(total_prices[currency]["prices"], currency) for currency in total_prices])
                + "\n\n__Current page entries:__\n"
                + "\n".join([entry_string(entry, timezone) for entry in chunk])
            )
            if len(chunk)
            else ""
        )
        embed.set_footer(text=f"Page {i+1}/{len(chunks)} • Total entries: {total_entries}")
        embeds.append(embed)
        
    return embeds

def bbt_list_grouped_embed(
    user_id: int,
    entries: list[dict],
    year: int | None,
    timezone: datetime.tzinfo,
    group_by: str,
    total_prices: dict = None,
    items_per_page: int = 10,
):
    organized_data = organize_entries_by_group(entries, group_by)
    embeds = []
    total_entries = len(entries)

    for group_name, group_data in organized_data.items():
        group_entries = group_data["entries"]
        chunks = [group_entries[i:i + items_per_page] for i in range(0, len(group_entries), items_per_page)]
        
        for i, chunk in enumerate(chunks):
            embed = discord.Embed(
                title=f"Bubble tea entries {f'for {year}' if year else 'for the past year'} grouped by {group_by} 🧋",
                color=discord.Color.blue(),
            )
            
            # Add total information
            embed.description = f"For <@{user_id}>: **{total_entries} total entries**"
            
            if i == 0:  # Only for first page of each group
                embed.description += "\n\n__Total costs (all entries)__:\n"
                embed.description += "\n".join([
                    cost_string(total_prices[currency]["prices"], currency) 
                    for currency in total_prices
                ])
            
            # Add group information
            embed.description += f"\n\n---\n**{group_name}: {len(group_entries)} entries**"
            for currency in group_data["prices"]:
                embed.description += f"\n{currency}: {cost_string(group_data['prices'][currency]['prices'], currency)}"
            
            # Add entries for this chunk
            embed.description += "\n\n"
            embed.description += "\n".join([
                entry_string(entry, timezone) 
                for entry in chunk
            ])
            
            embed.set_footer(text=f"Group: {group_name} • Page {i+1}/{len(chunks)} • Total entries: {total_entries}")
            embeds.append(embed)
    
    return embeds


def bbt_stats_embed(
    user_id: int,
    entries: list[dict],
    year: int,
    group_by_location: bool,
    monthly_counts: list[dict],
    latest: dict,
    timezone: datetime.tzinfo,
    total_entries: int = None,
):
    current_count = sum([len(entry.get("prices_list", [])) for entry in entries])
    embed = discord.Embed(
        title=f"Bubble tea stats {f'for {year}' if year else 'for the past year'} {'grouped by location ' if group_by_location else ''}🧋",
        color=discord.Color.green(),
    )
    embed.description = (
        f"For <@{user_id}>: **{total_entries or current_count} total entries**\n{average_year_string(year, total_entries or current_count)}\n\n"
    )
    if current_count > 0:
        embed.description += f"{'__Total costs__' if not group_by_location else '__Costs by location__'}:\n"
        embed.description += "\n".join(
            [
                (
                    "- "
                    + (f'**{entry.get("location")}**: ' if group_by_location else "")
                    + cost_string(
                        entry.get("prices_list") or [],
                        entry.get("currency"),
                    )
                    + (f'\n  - *{rating_string(entry)}*' if entry.get("average_rating") else "")
                )
                for entry in entries
            ]
        )

        if monthly_counts and not group_by_location:
            current_year = year if year else datetime.datetime.now().year
            embed.description += "\n\n__Monthly counts__:\n"
            embed.description += "\n".join(
                [
                    f"**{calendar.month_name[monthly_count.get('month', 0)]}**: {monthly_count.get('entry_count')} entries ({average_month_string(current_year, monthly_count.get('month', 0), monthly_count.get('entry_count'))})"
                    + ('\n- ' + rating_string(monthly_count) if monthly_count.get("average_rating") else "")
                    for monthly_count in monthly_counts
                ]
            )
        if latest and not group_by_location:
            embed.description += "\n\n**Latest entry**:\n"
            embed.description += entry_string(latest, timezone)
    return embed
