from babel import numbers, Locale
import discord
import datetime

locale = Locale("en", "US")


def bubble_tea_string(
    description: str, location: str, price: float, currency: str
):
    return f"{description}{f' at {location}' if location else ''}{f' for {price_string(price, currency)}' if price else ''} 🧋"


def price_string(price: float, currency: str):
    return (
        f"{numbers.format_currency(price, currency if currency else 'USD', locale='en_US')}"
        if price
        else "no specified price"
    )


def calculate_prices(entries: list[dict]):
    prices = {}
    for entry in entries:
        if not entry.get('price'):
            continue
        currency = entry.get('currency', 'USD')
        # store the number of entries for a given currency as well as the total
        if currency in prices:
            prices[currency]["count"] += 1
            prices[currency]["total"] += entry["price"]
        else:
            prices[currency] = {
                "count": 1,
                "total": entry["price"],
            }
    return prices


def bbt_embed(
    id: int,
    user_id: int,
    date: str,
    name: str,
    icon_url: str,
    entry: dict,
    new: bool = False,
):
    embed = discord.Embed(
        title=f"New bubble tea entry" if new else f"Bubble tea entry #{id}",
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
