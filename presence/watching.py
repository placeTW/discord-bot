from random import choice
import discord
from discord.app_commands import Choice
from discord import app_commands

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
)

MOVIE_CHOICES = [
    Choice(name=movie_name, value=movie_name) for movie_name in LIST_OF_MOVIES
]


def get_random_movie():
    return choice(LIST_OF_MOVIES)


def get_random_movie_as_activity():
    movie_name = get_random_movie()
    return discord.Activity(
        name=movie_name, type=discord.ActivityType.watching
    )


def register_commands(
    tree, this_guild: discord.Object, client: discord.Client
):
    @tree.command(
        name="set_watching",
        description="Sets the bot's status to 'Watching' (movie)...",
        guild=this_guild,
    )
    @app_commands.choices(movie_name=MOVIE_CHOICES)
    async def set_watching_status(
        interaction: discord.Interaction, movie_name: Choice[str]
    ):
        movie_activity = discord.Activity(
            name=movie_name.value, type=discord.ActivityType.watching
        )
        await client.change_presence(
            status=discord.Status.idle, activity=movie_activity
        )
        await interaction.response.send_message(
            f"Set bot status to 'Watching: {movie_name.value}'", ephemeral=True
        )
