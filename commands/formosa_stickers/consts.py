from discord.app_commands import Choice


SITE_URL = 'https://sticker.fpg.com.tw'

POSSIBLE_URLS = {
  'daily': f'{SITE_URL}/daily.aspx',
  'search': f'{SITE_URL}/search.aspx',
  'festival': f'{SITE_URL}/festival_all.aspx',
  'note': f'{SITE_URL}/note.aspx',
}

TYPES = {
  'daily': 'Daily',
  'search': 'Search',
  'festival': 'Festival',
  'note': 'Note',
}

TYPE_CHOICES = [
  Choice(name=desc, value=id) for id, desc in TYPES.items()
]

STYLE_TYPES = {
  'photo': 'Photo',
  'illustraton': 'Illustration',
  'short': 'Short (Gif)',
}

STYLE_TYPE_CHOICES = [
  Choice(name=desc, value=id) for id, desc in STYLE_TYPES.items()
]

TAGS = {
  'morning': '早安',
  'night': '晚安',
  'happy_holidays': '假日愉快',
  'new_year': '新年',
}

HOLIDAYS_TAGS = {
  'new_year': '新年',
  'valentines_day': '情人節',
  'lunar_new_year': '農曆新年',
  'lantern_festival': '元宵節',
  'labor_day': '勞動節',
  'mothers_day': '母親節',
  'fathers_day': '父親節',
  'dragon_boat_festival': '端午節',
  'taiwanese_valentines': '七夕',
  'ghost_festival': '中元節',
  'mid_autumn_festival': '中秋節',
  'double_ten_day': '雙十節',
  'winter_solstice': '冬至',
  'christmas': '聖誕節',
  'new_year_eve': '跨年',
}

HOLIDAYS_TAGS_TRANSLATIONS = {
  'new_year': 'New Year',
  'valentines_day': 'Valentine\'s Day',
  'lunar_new_year': 'Lunar New Year',
  'lantern_festival': 'Lantern Festival',
  'labor_day': 'Labor Day',
  'mothers_day': 'Mother\'s Day',
  'fathers_day': 'Father\'s Day',
  'dragon_boat_festival': 'Dragon Boat Festival',
  'taiwanese_valentines': 'Taiwanese Valentine\'s',
  'ghost_festival': 'Ghost Festival',
  'mid_autumn_festival': 'Mid-Autumn Festival',
  'double_ten_day': 'Double Ten Day',
  'winter_solstice': 'Winter Solstice',
  'christmas': 'Christmas',
  'new_year_eve': 'New Year\'s Eve',
}

HOLIDAYS_TAGS_CHOICES = [
  Choice(name=f'{desc} ({HOLIDAYS_TAGS_TRANSLATIONS[id]})', value=id) for id, desc in HOLIDAYS_TAGS.items()
]