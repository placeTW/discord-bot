import discord
from discord import app_commands


def register_commands(tree, guilds_dict: dict,):
    @tree.command(
        name="server_stats",
        description="Statistics on message events in this server",
        guilds=[
            discord.Object(id=int(server_id))
            for server_id in guilds_dict.keys()
        ],
    )
    @app_commands.describe(event="(Optional) The event to get stats for", user="(Optional) The user to get stats for", days="(Optional) The number of days to get stats for (default 7)")
    async def server_stats(interaction: discord.Interaction, event: str = None, user: discord.Member = None, days: int = 7):
        user_id = user.id if user is not None else interaction.user.id
        try:
            pass
        except:
            print(f'Could not get message stats for {event} and/or {user}')
        pass

    @tree.command(
        name="global_stats",
        description="Statistics on message events in all the servers that this bot is in",
        guilds=[
            discord.Object(id=int(server_id))
            for server_id in guilds_dict.keys()
        ],
    )
    @app_commands.describe(event="(Optional) The event to get stats for", user="(Optional) The user to get stats for", days="(Optional) The number of days to get stats for (default 7)")
    async def global_stats(interaction: discord.Interaction, event: str = None, user: discord.Member = None, days: int = 7):
        user_id = user.id if user is not None else interaction.user.id
        try:
            pass
        except:
            print(f'Could not get message stats for {event} and/or {user}')
        pass

    @tree.command(
        name="server_top",
        description="Top users in this server",
        guilds=[
            discord.Object(id=int(server_id))
            for server_id in guilds_dict.keys()
        ],
    )
    @app_commands.describe(event="(Optional) The event to get stats for", days="(Optional) The number of days to get stats for (default 7)", page="(Optional) The page number to get stats for")
    async def server_top(interaction: discord.Interaction, event: str = None, days: int = 7, page: int = 1):
        try:
            pass
        except:
            print(f'Could not get top stats for {event}')
        pass

    @tree.command(
        name="global_top",
        description="Top users in all the servers that this bot is in",
        guilds=[
            discord.Object(id=int(server_id))
            for server_id in guilds_dict.keys()
        ],
    )
    @app_commands.describe(event="(Optional) The event to get stats for", days="(Optional) The number of days to get stats for (default 7)", page="(Optional) The page number to get stats for")
    async def global_top(interaction: discord.Interaction, event: str = None, days: int = 7, page: int = 1):
        try:
            pass
        except:
            print(f'Could not get top stats for {event}')
        pass
