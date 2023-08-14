from random import choice
import discord
from discord.app_commands import Choice
from discord import app_commands

LIST_OF_GAMES = tuple()

GAME_CHOICES = [
    Choice(name=game_name, value=game_name) for game_name in LIST_OF_GAMES
]


def get_random_game():
    return choice(LIST_OF_GAMES)


def get_random_game_as_activity():
    game_name = get_random_game()
    return discord.Activity(name=game_name, type=discord.ActivityType.watching)


# ! not registered in main yet because not tested!
def register_commands(
    tree, this_guild: discord.Object, client: discord.Client
):
    @tree.command(
        name="set_watching",
        description="Sets the bot's status to 'Playing' (movie)...",
        guild=this_guild,
    )
    @app_commands.choices(movie_name=GAME_CHOICES)
    async def set_playing_status(
        interaction: discord.Interaction, movie_name: Choice[str]
    ):
        movie_activity = discord.Activity(
            name=movie_name.value,
            type=discord.ActivityType.playing,  # ! not tested yet
        )
        await client.change_presence(
            status=discord.Status.idle, activity=movie_activity
        )
        await interaction.response.send_message(
            f"Set bot status to 'Playing: {movie_name.value}'", ephemeral=True
        )
