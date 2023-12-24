from discord.app_commands import Choice


SITE_URL = 'https://sticker.fpg.com.tw'

POSSIBLE_URLS = {
  'daily': f'{SITE_URL}/daily.aspx',
  'search': f'{SITE_URL}/search.aspx',
  'festival': f'{SITE_URL}/festival_all.aspx',
  'note': f'{SITE_URL}/note.aspx',
  'search': f'{SITE_URL}/search.aspx',
}

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
}

POSSIBLE_TAGS = {
  'morning': {
    'query': '早安',
    'name': 'Good Morning',
  },
  'night': {
    'query': '晚安',
    'name': 'Good Night',
  },
  'happy_holidays': {
    'query': '假日愉快',
    'name': 'Happy Holidays',
  },
}