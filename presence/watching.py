from random import choice
import discord
from discord.app_commands import Choice
from discord import app_commands
from .watching_consts import LIST_OF_MOVIES, MOVIE_CHOICES


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
            status=discord.Status.online, activity=movie_activity
        )
        await interaction.response.send_message(
            f"Set bot status to 'Watching: {movie_name.value}'", ephemeral=True
        )
