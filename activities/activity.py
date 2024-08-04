from random import choice
import discord
from discord.app_commands import Choice
from discord import app_commands
from .watching_consts import LIST_OF_MOVIES
from .playing_consts import LIST_OF_GAMES

ACTIVITIES_DICT = {
    "watching": LIST_OF_MOVIES,
    "playing": LIST_OF_GAMES,
    # "listening", # ! not supported yet
    # "streaming", # ! not supported yet
}
ACTIVITY_TYPES = list(ACTIVITIES_DICT.keys())
ACTIVITY_CHOICES = [Choice(name=activity_type, value=activity_type) for activity_type in ACTIVITY_TYPES]


def get_random_activity_type():
    return choice(ACTIVITY_TYPES)


def get_activity_item(activity_type: str, index: int = None):
    """
    Returns a random activity item based on the activity type.
    If index is provided, returns the item at that index.
    Otherwise, returns a random item.
    """
    assert activity_type in ACTIVITY_TYPES, f"Invalid activity type: {activity_type}. Allowed types: {ACTIVITY_TYPES}"
    if activity_type == "watching":
        return LIST_OF_MOVIES[index] if index is not None else choice(LIST_OF_MOVIES)
    elif activity_type == "playing":
        return LIST_OF_GAMES[index] if index is not None else choice(LIST_OF_GAMES)


def get_random_activity_as_discordpy_activity():
    # get random activity type, then get random item from that activity type, then return it as a discord.Activity object
    activity_type = get_random_activity_type()
    activity_name = get_activity_item(activity_type)
    if activity_type == "watching":
        return discord.Activity(name=activity_name, type=discord.ActivityType.watching)
    elif activity_type == "playing":
        return discord.Activity(name=activity_name, type=discord.ActivityType.playing)


def register_commands(tree, this_guild: discord.Object, client: discord.Client):
    @tree.command(
        name="set_activity",
        description=f"Sets the bot's status to an activity type (see: `/list_activities` and `/list_activity_items`).",
        guild=this_guild,
    )
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.choices(activity_choice=ACTIVITY_CHOICES)
    @app_commands.describe(activity_choice="The activity type to set the bot's status to (random if not specified)")
    @app_commands.describe(
        activity_index="The index of the activity item to set the bot's status to (random if not specified)"
    )
    async def set_activity(
        interaction: discord.Interaction, activity_choice: Choice[str] = None, activity_index: int = None
    ):
        # if activity_index is provided but activity_choice is not, then it's an error
        if activity_index is not None and activity_choice is None:
            await interaction.response.send_message(
                "You must provide the activity type if you want to set the activity index.", ephemeral=True
            )
            return
        activity_type = get_random_activity_type() if activity_choice is None else activity_choice.value
        activity_list_to_use = ACTIVITIES_DICT[activity_type]
        if activity_index is not None and activity_index < 0 and activity_index >= len(activity_list_to_use):
            await interaction.response.send_message("Invalid activity index. Please try again.", ephemeral=True)
            return
        activity_name = (
            activity_list_to_use[activity_index] if activity_index is not None else get_activity_item(activity_type)
        )
        await interaction.response.send_message(
            f"Set bot status to '{activity_type}' with value '{activity_name}' (index: {activity_index})"
        )
        if activity_type == "watching":
            activity = discord.Activity(name=activity_name, type=discord.ActivityType.watching)
        elif activity_type == "playing":
            activity = discord.Activity(name=activity_name, type=discord.ActivityType.playing)
        await client.change_presence(activity=activity)

    @tree.command(
        name="list_activities",
        description="Lists all the activities that the bot can do.",
        guild=this_guild,
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def list_activities(interaction: discord.Interaction):
        activity_list = "\n".join([f"* {activity_type}" for activity_type in ACTIVITY_TYPES])
        await interaction.response.send_message(
            f"Here are the activities that the bot can do:\n{activity_list}",
        )

    @tree.command(
        name="list_activity_items",
        description="Lists all the items for a specific activity.",
        guild=this_guild,
    )
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.choices(activity_choice=ACTIVITY_CHOICES)
    @app_commands.describe(activity_choice="The activity type to list the items for")
    async def list_activity_items(interaction: discord.Interaction, activity_choice: Choice[str]):
        activity_type = activity_choice.value
        activity_list = "\n".join([f"{i}: {activity}" for i, activity in enumerate(ACTIVITIES_DICT[activity_type])])
        await interaction.response.send_message(
            f"Here are the items for the activity type `{activity_type}`:\n{activity_list}",
        )
