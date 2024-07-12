# from random import choice
# import discord
# from discord.app_commands import Choice
# from discord import app_commands
# from .watching_consts import LIST_OF_MOVIES

# def get_random_movie():
#     return choice(LIST_OF_MOVIES)

# def register_commands(
#     tree, this_guild: discord.Object, client: discord.Client
# ):
#     @tree.command(
#         name="set_watching",
#         description=f"Sets the bot's status to 'Watching' (movie) using a movie's index (/{LIST_MOVIES_CMD_NAME}).",
#         guild=this_guild,
#     )
#     @app_commands.checks.has_permissions(administrator=True)
#     async def set_watching_status(
#         interaction: discord.Interaction, movie_index: int
#     ):
#         if movie_index < 0 or movie_index >= len(LIST_OF_MOVIES):
#             await interaction.response.send_message(
#                 "Invalid movie index. Please try again.", ephemeral=True
#             )
#             return
#         movie_name = LIST_OF_MOVIES[movie_index]
#         movie_activity = discord.Activity(
#             name=movie_name, type=discord.ActivityType.watching
#         )
#         await client.change_presence(activity=movie_activity)
#         await interaction.response.send_message(
#             f"Set bot status to 'Watching: {movie_name}'", ephemeral=True
#         )

#     @tree.command(
#         name="list_movies",
#         description="Lists all the movies that the bot can watch.",
#         guild=this_guild,
#     )
#     @app_commands.checks.has_permissions(administrator=True)
#     async def list_movies(interaction: discord.Interaction):
#         movie_list = "\n".join([f"{i}: {movie}" for i, movie in enumerate(LIST_OF_MOVIES)])
#         await interaction.response.send_message(
#             f"Here are the movies that the bot can watch:\n{movie_list}",
#             # ephemeral=True,
#         )