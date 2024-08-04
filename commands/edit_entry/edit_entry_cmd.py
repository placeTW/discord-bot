import discord
from discord import app_commands

from commands.fetch_entry.fetch_entry_main import _fetch_entry_with_json
from modules import async_utils
from discord.app_commands import Choice
from .interfaces import submit_entry_modal

# from .fetch_entry_main import _fetch_entry_with_json

from ..entry_consts.consts import (
    POSSIBLE_ART2023_IDS,
    POSSIBLE_LANGUAGE_CODES,
    POSSIBLE_ART_FIELD_CODES,
)


def register_commands(tree, this_guild: discord.Object, client: discord.Client):
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
        entry: Choice[str],
        lang: Choice[str],
        field: Choice[str],  # field CANNOT be empty in this case
    ):
        # * assemble values
        selected_lang = lang.value  # lang always exists
        selected_entry_id = entry.value  # entry always exists
        selected_entry_name = entry.name  # entry always exists
        selected_field = field.value  # field is mandatory here
        initial_value = await _fetch_entry_with_json(
            interaction, selected_entry_id, selected_lang, selected_field, fromI18n=True
        )
        form = submit_entry_modal.SubmitEntryModal(
            client,
            "Entry Edit Submission",
            selected_lang,
            selected_entry_id,
            selected_entry_name,
            selected_field,
            ",".join(initial_value) if isinstance(initial_value, list) else initial_value,
        )

        await interaction.response.send_modal(form)


if __name__ == "__main__":
    import asyncio

    link = "https://placetw.com/locales/en/art-pieces.json"
    asyncio.run(async_utils._async_get_json(link))
