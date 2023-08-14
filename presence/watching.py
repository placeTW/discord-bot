from random import choice
import discord

LIST_OF_MOVIES = (
    "City of Sadness / 悲情城市",
    "7 Days in Heaven / 父後七日",
    "Detention / 返校",
)


def get_random_movie():
    return choice(LIST_OF_MOVIES)


def get_random_movie_as_activity():
    movie_name = get_random_movie()
    return discord.Activity(
        name=movie_name, type=discord.ActivityType.watching
    )
