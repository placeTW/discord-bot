
from babel import numbers, Locale

locale = Locale('en', 'US')


def bubble_tea_string(description: str, location: str, price: float, currency: str):
    return f"{description}{f' at {location}' if location else ''}{f' for {price_string(price, currency)}' if price else ''} 🧋"

def price_string(price: float, currency: str):
    return f"{numbers.format_currency(price, currency if currency else 'USD', locale='en_US')}" if price else 'no specified price'

def calculate_prices(entries: list[dict]):
    prices = {}
    for entry in entries:
        if not entry['price']:
            continue
        currency = entry['currency'] if entry['currency'] else 'USD'
        # store the number of entries for a given currency as well as the total
        if currency in prices:
            prices[currency]['count'] += 1
            prices[currency]['total'] += entry['price']
        else:
            prices[currency] = {
                'count': 1,
                'total': entry['price'],
            }
    return prices