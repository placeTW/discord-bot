import aiohttp
import discord
from discord import app_commands
from ..modules import async_utils, postprocess
import typing
from discord.app_commands import Choice

# from .fetch_entry_main import _fetch_entry_with_json

from ..entry_consts.consts import (
    POSSIBLE_ART2023_IDS,
    POSSIBLE_LANGUAGE_CODES,
    POSSIBLE_ART_FIELD_CODES,
)

# channel to receive approval requests
WAITING_APPROVAL_CHANNEL_ID = 1135250604751601716


class SubmitEntryModal(discord.ui.Modal):
    def __init__(
        self,
        client: discord.Client,
        lang: str,
        entry_id: int,
        entry_name: str,
        title: str,
        field: str,
        *,
        timeout: float = None,
    ) -> None:
        super().__init__(title=title, timeout=timeout)
        self.the_client = client
        self.approval_channel = client.get_channel(WAITING_APPROVAL_CHANNEL_ID)
        self.proposed_entry = discord.ui.TextInput(
            label=f"New entry for entry: {entry_name} language: {lang} field: {field}",
            style=discord.TextStyle.paragraph,
            min_length=1,
            placeholder="Enter the new entry here",
        )
        self.add_item(self.proposed_entry)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Thanks for your response! The team will review your request soon.",
            ephemeral=True,
        )
        user_name = interaction.user.name
        await self.approval_channel.send(
            f"user {user_name} sent `{self.proposed_entry.value}`"
        )


def register_commands(
    tree, this_guild: discord.Object, client: discord.Client
):
    @tree.command(
        name="edit-entry",
        description="Changes an entry for an art piece.",
        guild=this_guild,
    )
    @app_commands.choices(entry=POSSIBLE_ART2023_IDS)
    @app_commands.choices(lang=POSSIBLE_LANGUAGE_CODES)
    @app_commands.choices(field=POSSIBLE_ART_FIELD_CODES)
    @app_commands.checks.has_any_role("admin", "translator", "dev")
    async def edit_entry_cmd(
        interaction: discord.Interaction,
        entry: Choice[int],
        lang: Choice[str],
        field: Choice[str],  # field CANNOT be empty in this case
    ):
        # * assemble values
        selected_lang = lang.value  # lang always exists
        selected_entry_id = entry.value  # entry always exists
        selected_entry_name = entry.name  # entry always exists
        selected_field = field.value  # field is mandatory here
        form = SubmitEntryModal(
            client,
            "Entry Edit Submission",
            selected_lang,
            selected_entry_id,
            selected_entry_name,
            selected_field,
        )

        await interaction.response.send_modal(form)


if __name__ == "__main__":
    import asyncio

    link = "https://placetw.com/locales/en/art-pieces.json"
    asyncio.run(async_utils._async_get_json(link))
