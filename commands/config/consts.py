from discord.app_commands import Choice


SUPPORTED_CHANNEL_CONFIG_FIELDS = {
    "confession_channel_id": "Confession Channel",
    "report_channel_id": "Report Channel",
}

POSSIBLE_CHANNEL_CONFIG_FIELDS = [
    Choice(name=desc, value=field) for field, desc in SUPPORTED_CHANNEL_CONFIG_FIELDS.items()
]
