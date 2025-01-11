from babel import numbers, Locale
import datetime
import numpy as np
import calendar

locale = Locale("en", "US")


def bubble_tea_data(
    description: str,
    user_id: int,
    created_at: datetime.datetime,
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
    if created_at:
        data["created_at"] = created_at
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


def bubble_tea_string(description: str, location: str, price: float, currency: str):
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
            key=lambda item: sum(len(currency["prices"]) for currency in item[1].values()),
            reverse=True,
        )
    )

    return prices

def organize_entries_by_group(entries: list[dict], group_by: str = None):
    """Organize entries into groups and calculate statistics"""
    if not group_by:
        return {
            "default_group": {
                "entries": entries,
                "prices": calculate_prices(entries, None)["default_group"]
            }
        }
    
    groups = {}
    for entry in entries:
        group_key = entry.get(group_by, "Unknown")
        if group_key not in groups:
            groups[group_key] = {
                "entries": [],
                "prices": {}
            }
        groups[group_key]["entries"].append(entry)
    
    # Calculate prices for each group
    for group_key, group_data in groups.items():
        group_data["prices"] = calculate_prices(group_data["entries"], None)["default_group"]
    
    # Sort groups by number of entries
    return dict(sorted(
        groups.items(),
        key=lambda x: len(x[1]["entries"]),
        reverse=True
    ))

def cost_string(prices: list[float], currency: str):
    p = np.array(prices)
    sum = p[p != np.array(None)].sum()
    return f"{numbers.format_currency(sum, currency, locale='en_US')} ({p.size}, avg {numbers.format_currency(p[p.nonzero()].mean() if sum else 0, currency, locale='en_US')}/🧋)"


def entry_string(entry: dict, timezone: datetime.tzinfo):
    entry_string = (
        f"`{entry['id']}: {str(datetime.datetime.fromisoformat(entry.get('created_at')).astimezone(timezone).date())}`"
    )
    entry_string += f" - {bubble_tea_string(entry.get('description'), entry.get('location'), entry.get('price'), entry.get('currency'))}"
    entry_string += f"{' (no image)' if not entry.get('image') else ''}"
    entry_string += f"{' *rating: ' + str(entry.get('rating')) + '*' if entry.get('rating') else ''}"
    entry_string += f" {'notes: ' + entry.get('notes') if entry.get('notes') else ''}"
    return entry_string.strip()


def average_string(days: int, entry_count: int, is_current: bool):
    return (
        f"Average of 1 🧋 every {days/entry_count:.3f} days {'*so far*' if is_current else ''}".strip()
        if days and entry_count
        else "Average of 0 🧋"
    )


def average_year_string(year: int, entry_count: int):
    days = (
        (datetime.date.today() if not year or year == datetime.date.today().year else datetime.date(year, 12, 31))
        - datetime.date(year or datetime.date.today().year, 1, 1)
    ).days + 1
    is_current = not year or year == datetime.date.today().year
    return average_string(days, entry_count, is_current)


def average_month_string(year: int, month: int, entry_count: int):
    ## check if the year and month are the current year and month, and if so, use the days from the beginning to the current date
    days = (
        (
            datetime.date.today()
            if (not year or year == datetime.date.today().year) and month == datetime.date.today().month
            else datetime.date(year, month, calendar.monthrange(year, month)[1])
        )
        - datetime.date(year or datetime.date.today().year, month, 1)
    ).days + 1
    is_current = (not year or year == datetime.date.today().year) and month == datetime.date.today().month
    return average_string(days, entry_count, is_current)


def rating_string(entry: dict):
    return (
        'ratings: '
        + (f"min: {entry.get('minimum_rating'):.3f}, " if entry.get("minimum_rating") else "")
        + (f"avg: {entry.get('average_rating'):.3f}, " if entry.get("average_rating") else "")
        + (f"max: {entry.get('maximum_rating'):.3f}" if entry.get("maximum_rating") else "")
    )
