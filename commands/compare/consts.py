from discord.app_commands import Choice

CITIES_DICT = {
    "TW, Taipei": {
        "city_name": "Taipei", # for numbeo
        "country": "Taiwan", # for numbeo
    },
    "TW, Kaohsiung": {
        "city_name": "Kaohsiung",
        "country": "Taiwan",
    },
    "CA, Ottawa": {
        "city_name": "Ottawa",
        "country": "Canada",
    },
    "JP, Tokyo": {
        "city_name": "Tokyo",
        "country": "Japan",
    },
    "LT, Vilnius": {
        "city_name": "Vilnius",
        "country": "Lithuania",
    },
    "LV, Riga": {
        "city_name": "Riga",
        "country": "Latvia",
    },
    "EE, Tallinn": {
        "city_name": "Tallinn",
        "country": "Estonia",
    },
    "UK, London": {
        "city_name": "London",
        "country": "United Kingdom",
    },
    "FR, Paris": {
        "city_name": "Paris",
        "country": "France",
    },
    "DE, Berlin": {
        "city_name": "Berlin",
        "country": "Germany",
    },
    "AU, Sydney": {
        "city_name": "Sydney",
        "country": "Australia",
    },
}

CITIES_CHOICES = [Choice(name=city_choice, value=city_choice) for city_choice in CITIES_DICT.keys()]