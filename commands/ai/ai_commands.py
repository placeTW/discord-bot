from discord import app_commands
import discord
from modules.ai.llm import get_response, list_models
from utils.splitter import split_text

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
    async def llm(interaction: discord.Interaction, question: str, model: str = ""):
        await interaction.response.defer()
        try:
            response = get_response(question, model)
            split_response = split_text(response)
            for chunk in split_response:
                await interaction.followup.send(chunk)
        except Exception as e:
            await interaction.followup.send(f"An error occurred: {e}")

    @tree.command(
        name="llm_models",
        description="List available models",
        guilds=guilds,
    )
    async def llm_models(interaction: discord.Interaction):
        await interaction.response.defer()
        try:
            models = list_models()
            await interaction.followup.send("\n".join(models))
        except Exception as e:
            await interaction.followup.send(f"An error occurred: {e}")