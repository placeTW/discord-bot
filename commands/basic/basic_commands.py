from discord import app_commands

import discord


def register_commands(
    tree: discord.app_commands.CommandTree,
    guilds: list[discord.Object],
):
    @tree.command(
        name="website",
        description="Responds with the placeTW website link",
        guilds=guilds,
    )
    async def website(interaction: discord.Interaction):
        await interaction.response.send_message("https://placetw.com/")

    @tree.command(
        name="invite",
        description="Invite this bot to your server!",
        guilds=guilds,
    )
    async def invite_link(interaction: discord.Interaction):
        await interaction.response.send_message(
            "https://discord.com/oauth2/authorize?client_id=1134650883637006407&&permissions=2147484672&scope=bot"
        )

    @tree.command(
        name="echo",
        description="Echoes whatever string is fed",
        guilds=guilds,
    )
    @app_commands.describe(given_str="The string you want echoed backed")
    async def echo(interaction: discord.Interaction, given_str: str):
        await interaction.response.send_message(f"You sent this: `{given_str}`")
