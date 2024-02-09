
from discord import app_commands
import discord

def register_commands(
    tree: app_commands.CommandTree,
):
    @tree.command(
        name="website",
        description="Responds with the placeTW website link",
    )
    async def website(interaction: discord.Interaction):
        await interaction.response.send_message("https://placetw.com/")


    @tree.command(
        name="invite",
        description="Invite this bot to your server!",
    )
    async def invite_link(interaction: discord.Interaction):
        await interaction.response.send_message("https://discord.com/oauth2/authorize?client_id=1134650883637006407&&permissions=2147484672&scope=bot")

    @tree.command(
        name="echo",
        description="Echoes whatever string is fed",
    )
    @app_commands.describe(given_str="The string you want echoed backed")
    async def echo(interaction: discord.Interaction, given_str: str):
        await interaction.response.send_message(f"You sent this: `{given_str}`")