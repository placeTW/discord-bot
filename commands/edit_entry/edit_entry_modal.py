from typing import Optional
import discord
from discord import ui
from discord.utils import MISSING

WAITING_APPROVAL_CHANNEL_ID = 1135250604751601716


class Questionnaire(ui.Modal):
    name = ui.TextInput(label="Name")
    answer = ui.TextInput(label="Answer", style=discord.TextStyle.paragraph)

    def __init__(
        self,
        client: discord.Client,
        *,
        title: str,
        timeout: float = None,
    ) -> None:
        super().__init__(title=title, timeout=timeout)
        self.the_client = client
        self.approval_channel = client.get_channel(WAITING_APPROVAL_CHANNEL_ID)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Thanks for your response, {self.name}!", ephemeral=True
        )
        user_name = interaction.user.name
        await self.approval_channel.send(
            f"user {user_name} sent `{self.answer}`"
        )


def register_commands(
    tree, this_guild: discord.Object, client: discord.Client
):
    @tree.command(
        name="edit-entry",
        description="Edits an entry via form",
        guild=this_guild,
    )
    async def call_form(interaction: discord.Interaction):
        form = Questionnaire(client, title="Questionnaire")
        await interaction.response.send_modal(form)
