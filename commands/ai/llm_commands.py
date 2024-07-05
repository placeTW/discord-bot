from discord import app_commands
import discord
from modules.ai.llm import get_response

def register_commands(
    tree: discord.app_commands.CommandTree,
    guilds: list[discord.Object],
):
    @tree.command(
        name="llm",
        description="Ask the AI a question",
        guilds=guilds,
    )
    @app_commands.describe(question="The question you want to ask the AI")
    async def llm(interaction: discord.Interaction, question: str):
        await interaction.response.defer()
        response = get_response(question)
        await interaction.followup.send(response)