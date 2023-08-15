from discord.app_commands import Choice


LIST_OF_MOVIES = (
    "City of Sadness / 悲情城市",
    "7 Days in Heaven / 父後七日",
    "Detention / 返校",
    "Cape No. 7 / 海角七號",
    "The World Between Us / 我們與惡的距離",
    "Spicy Teacher / 麻辣鮮師",
    "Warriors Of The Rainbow / 賽德克·巴萊",
    "The Teenage Psychic / 通靈少女",
    "KANO (2014)",
    "Incantation / 咒",
    "You Are the Apple of My Eye / 那些年，我們一起追的女孩",
    "Din Tao: Leader of the Parade / 陣頭",
    "Light the Night / 華燈初上",
    "Gold Leaf / 茶金",
    "Alifu / 阿里夫/芙",
    "Your Name Engraved Herein / 刻在我心底的名字",
    "Our Times / 我的少女時代",
    "The Dull-Ice Flower / 魯冰花",
    "Zone Pro Site / 總舖師",
    "Beyond Beauty: Taiwan from Above / 看見台灣",
    "Monga / 艋舺",
    "The Tag-Along / 紅衣小女孩",
    "Till We Meet Again / 月老",
)

MOVIE_CHOICES = [
    Choice(name=movie_name, value=movie_name) for movie_name in LIST_OF_MOVIES
]
