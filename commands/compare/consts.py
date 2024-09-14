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
}

CITIES_CHOICES = [Choice(name=city_choice, value=city_choice) for city_choice in CITIES_DICT.keys()]