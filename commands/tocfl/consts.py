from discord.app_commands import Choice


TOCFL_LEVELS = {
    1: "Novice 1 (準備級一級)",
    2: "Novice 2 (準備級二級)",
    3: "Level 1 (入門級)",
    4: "Level 2 (基礎級)",
    5: "Level 3 (進階級)",
    6: "Level 4 (高階級)",
}

TOCFL_LEVELS_CHOICES = [
    Choice(name=level_name, value=level_num)
    for level_num, level_name in TOCFL_LEVELS.items()
]
