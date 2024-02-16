from babel import numbers, Locale
import datetime
import numpy as np

locale = Locale("en", "US")


def bubble_tea_data(
    description: str,
    user_id: int,
    location: str,
    price: float,
    currency: str,
    image: str,
    notes: str,
    rating: float,
):
    data = {}
    if description:
        data["description"] = description
    if user_id:
        data["user_id"] = user_id
    if location:
        data["location"] = location
    if price:
        data["price"] = price
    if currency:
        data["currency"] = currency
    if image:
        data["image"] = image
    if notes:
        data["notes"] = notes
    if rating:
        data["rating"] = rating
    return data


def bubble_tea_string(
    description: str, location: str, price: float, currency: str
):
    return f"**{description}**{f' at __{location}__' if location else ''}{f' for {price_string(price, currency)}' if price else ''}"


def price_string(price: float, currency: str):
    return (
        f"{numbers.format_currency(price, currency if currency else 'USD', locale='en_US')}"
        if price
        else "no specified price"
    )


def calculate_prices(entries: list[dict], group_by: str):
    prices = {}
    for entry in entries:
        price = entry.get("price") or 0
        currency = entry.get("currency", None)
        group_key = entry.get(group_by, "default_group")

        if group_key in prices:
            if currency in prices[group_key]:
                prices[group_key][currency]["prices"].append(price)
            else:
                prices[group_key][currency] = {
                    "prices": [price],
                }
        else:
            prices[group_key] = {
                currency: {
                    "prices": [price],
                }
            }
    # sort the groups by the amount of prices
    prices = dict(
        sorted(
            prices.items(),
            key=lambda item: sum(
                len(currency["prices"]) for currency in item[1].values()
            ),
            reverse=True,
        )
    )

    return prices


def cost_string_prices(prices: list[int], currency: str):
    p = np.array(prices)
    return cost_string(p.sum(), p.size, currency)


def cost_string(total_price: float, count: int, currency: str):
    return f"{numbers.format_currency(total_price, currency, locale='en_US')} ({count}, avg {numbers.format_currency(total_price/count if total_price and count else 0, currency, locale='en_US')}/🧋)"


def entry_string(entry: dict, timezone: datetime.tzinfo):
    entry_string = f"`{entry['id']}: {str(datetime.datetime.fromisoformat(entry.get('created_at')).astimezone(timezone).date())}`"
    entry_string += f" - {bubble_tea_string(entry.get('description'), entry.get('location'), entry.get('price'), entry.get('currency'))}"
    entry_string += f"{' (no image)' if not entry.get('image') else ''}"
    entry_string += f"{' *rating: ' + str(entry.get('rating')) + '*' if entry.get('rating') else ''}"
    entry_string += (
        f" {'notes: ' + entry.get('notes') if entry.get('notes') else ''}"
    )
    return entry_string.strip()


def average_string(days: int, entry_count: int):
    return (
        f"Average of 1 🧋 every {days/entry_count:.3f} days"
        if days and entry_count
        else "Average of 0 🧋"
    )


def average_year_string(year: int, entry_count: int):
    days = (
        (
            datetime.date.today()
            if not year or year == datetime.date.today().year
            else datetime.date(year, 12, 31)
        )
        - datetime.date(year or datetime.date.today().year, 1, 1)
    ).days
    return average_string(days, entry_count)
