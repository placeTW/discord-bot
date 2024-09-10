from discord.app_commands import Choice

METRO_DICT = {
    "Taipei" : "https://www.travel.taipei/Content/images/static/travel-tips/metrotaipeimap.jpg",
    "Kaohsiung": "https://www.krtc.com.tw/Content/userfiles/images/guide-map.jpg?v=0630",
    "Taoyuan": "https://www.travel.taipei/Content/images/static/information/tymetro-system-2.jpg",
    "Taichung": "https://tmrt.traffictw.com/_next/image?url=https%3A%2F%2Fwww.traffictw.com%2Fimage%2Ftmrt%2Fmap.jpg&w=1920&q=75",
}

METRO_CHOICES = [Choice(name=metro_name, value=metro_name) for metro_name, metro_url in METRO_DICT.items()]
