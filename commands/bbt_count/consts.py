from discord.app_commands import Choice

BBT_LIST_GROUP_BY = {
    "location": "Location",
    "currency": "Currency",
}

BBT_LIST_GROUP_BY_CHOICES = [
    Choice(name=desc, value=field) for field, desc in BBT_LIST_GROUP_BY.items()
]
