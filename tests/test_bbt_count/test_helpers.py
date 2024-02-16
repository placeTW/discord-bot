from commands.bbt_count.helpers import (
    bubble_tea_string,
    price_string,
    calculate_prices,
    cost_string_prices,
    entry_string,
)


entries = [
    {
        "description": "Classic Milk Tea",
        "location": "ABC Cafe",
        "price": 3.5,
        "currency": "USD",
    },
    {
        "description": "Brown Sugar Milk Tea",
        "location": "ABC Cafe",
        "price": 4.0,
        "currency": "CAD",
    },
    {
        "description": "Oolong Milk Tea",
        "location": "XYZ Cafe",
        "price": 3.0,
        "currency": "USD",
    },
    {
        "description": "Random Milk Tea",
        "location": "Test Cafe",
        "price": None,
        "currency": None,
    },
]

def test_bubble_tea_string():
    description = "Classic Milk Tea"
    location = "ABC Cafe"
    price = 3.5
    currency = "CAD"
    expected_result = "**Classic Milk Tea** at __ABC Cafe__ for CA$3.50"
    assert (
        bubble_tea_string(description, location, price, currency)
        == expected_result
    )


def test_price_string():
    price = 3.5
    currency = "CAD"
    expected_result = "CA$3.50"
    assert price_string(price, currency) == expected_result


def test_calculate_prices_no_group():
    group_by = None
    expected_result = {
        "default_group": {
            "USD": {"prices": [3.5, 3.0]},
            "CAD": {"prices": [4.0]},
            None: {"prices": [0]},
        }
    }
    assert calculate_prices(entries, group_by) == expected_result


def test_calculate_prices_group_by_location():
    group_by = "location"
    expected_result = {
        "ABC Cafe": {
            "USD": {"prices": [3.5]},
            "CAD": {"prices": [4.0]},
        },
        "XYZ Cafe": {
            "USD": {"prices": [3.0]},
        },
        "Test Cafe": {
            None: {"prices": [0]},
        },
    }
    assert calculate_prices(entries, group_by) == expected_result


def test_calculate_prices_group_by_currency():
    group_by = "currency"
    expected_result = {
        "USD": {
            "USD": {"prices": [3.5, 3.0]},
        },
        "CAD": {
            "CAD": {"prices": [4.0]},
        },
        None: {
            None: {"prices": [0]},
        },
    }
    assert calculate_prices(entries, group_by) == expected_result


def test_cost_string():
    prices = [3.5, 4.0, 3.0, 0]
    currency = "USD"
    expected_result = "$10.50 (4, avg $3.50/🧋)"
    assert cost_string_prices(prices, currency) == expected_result


def test_entry_string():
    entry = {
        "id": 1,
        "created_at": "2021-10-01T00:00:00",
        "description": "Classic Milk Tea",
        "location": "ABC Cafe",
        "price": 3.5,
        "currency": "CAD",
        "notes": "This is a classic milk tea with pearls. It's a little sweet, but not too much.",
        "rating": 4.5,
        "image": None,
    }
    expected_result = "`1: 2021-10-01` - **Classic Milk Tea** at __ABC Cafe__ for CA$3.50 (no image) *rating: 4.5* notes: This is a classic milk tea with pearls. It's a little sweet, but not too much."
    assert entry_string(entry, None) == expected_result
