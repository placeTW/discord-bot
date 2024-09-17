from discord.app_commands import Choice

TRAINS_DICT = {
    "Taipei" : "https://www.travel.taipei/Content/images/static/travel-tips/metrotaipeimap.jpg",
    "Kaohsiung": "https://www.krtc.com.tw/Content/userfiles/images/guide-map.jpg?v=0630",
    "Taoyuan": "https://www.travel.taipei/Content/images/static/information/tymetro-system-2.jpg",
    "Taichung": "https://tmrt.traffictw.com/_next/image?url=https%3A%2F%2Fwww.traffictw.com%2Fimage%2Ftmrt%2Fmap.jpg&w=1920&q=75",
    "THSR": "https://upload.wikimedia.org/wikipedia/commons/7/71/TaiwanHighSpeedRail_Route_Map_2022.png"
}

TRAINS_CHOICES = [Choice(name=train_name, value=train_name) for train_name, train_url in TRAINS_DICT.items()]
