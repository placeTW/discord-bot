from typing import Optional
import discord
from discord import ui
from discord.utils import MISSING


class Questionnaire(ui.Modal):
    name = ui.TextInput(label="Name")
    answer = ui.TextInput(label="Answer", style=discord.TextStyle.paragraph)

    def __init__(
        self,
        *,
        title: str,
        timeout: float = None,
    ) -> None:
        super().__init__(title=title, timeout=timeout)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Thanks for your response, {self.name}!", ephemeral=True
        )


def register_commands(tree, this_guild: discord.Object):
    @tree.command(
        name="edit-entry",
        description="Edits an entry via form",
        guild=this_guild,
    )
    async def call_form(interaction: discord.Interaction):
        form = Questionnaire(title="Questionnaire")
        await interaction.response.send_modal(form)
