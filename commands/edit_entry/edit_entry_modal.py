"""
NOTE: This file was created before I realised that you could
      only put in text fields for modals.
      As a result, this code will not be used until discord
      supports using selects, otherwise users would have to
      manually fill out the art_id and other fields,
      which would be a giant pain.
! basically: don't use this file!
"""
from typing import Optional
from ..entry_consts.consts import SUPPORTED_ART2023_IDS
import discord
from discord import ui
from discord.utils import MISSING


# channel to receive approval requests
WAITING_APPROVAL_CHANNEL_ID = 1135250604751601716


class Questionnaire(ui.Modal):
    proposed_entry = ui.TextInput(
        label="New entry",
        style=discord.TextStyle.paragraph,
    )

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
            f"Thanks for your response!", ephemeral=True
        )
        user_name = interaction.user.name
        await self.approval_channel.send(
            f"x`user {user_name} sent `{self.proposed_entry}`"
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
