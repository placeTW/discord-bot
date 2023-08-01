import asyncio
import discord
from discord import app_commands
from ..modules import async_utils, postprocess
import typing
from discord.app_commands import Choice
from .fetch_entry_main import _fetch_entry_with_json

from .consts import (
    SUPPORTED_ART2023_IDS,
    POSSIBLE_ART2023_IDS,
    SUPPORTED_ART_FIELDS,
    POSSIBLE_LANGUAGE_CODES,
    SUPPORTED_LANGUAGE_CODES,
)


# for views tutorial: see
class FetchEntryView(discord.ui.View):
    def __init__(self):
        super().__init__()
        # these are for storing the user's choices
        self.selected_entry = None
        self.selected_language = None
        self.selected_field = None

    # * There should be fields for:
    # * - entry (drop down menu), done
    # * - lang (drop down menu), done
    # * - field (drop down menu), done
    # * - year (drop down menu, only has 2023 atm)
    # * - submit (button), done

    @discord.ui.select(
        placeholder="Choose an entry",
        options=[
            discord.SelectOption(
                label=entry_id, description=entry_desc, value=i
            )
            for i, (entry_id, entry_desc) in enumerate(
                SUPPORTED_ART2023_IDS.items()
            )
        ],
        row=1,
    )
    async def select_entry_callback(
        self, interaction: discord.Interaction, select: discord.ui.Select
    ):
        # either the chosen value or None
        self.selected_entry = select.values[0]
        return await interaction.response.defer()  # i.e. "do nothing"

    @discord.ui.select(
        placeholder="Choose a language",
        options=[
            discord.SelectOption(label=lang_id, description=lang_id)
            for lang_id in SUPPORTED_LANGUAGE_CODES
        ],
        row=2,
    )
    async def select_lang_callback(
        self, interaction: discord.Interaction, select: discord.ui.Select
    ):
        # either the chosen value or None
        self.selected_language = select.values[0]
        return await interaction.response.defer()  # i.e. "do nothing"

    @discord.ui.select(
        placeholder="Choose a field (leave empty to fetch entire entry)",
        options=[
            discord.SelectOption(label=field_id, description=field_id)
            for field_id in SUPPORTED_ART_FIELDS + ["fetch entire entry"]
        ],
        row=3,
    )
    async def select_field_callback(
        self, interaction: discord.Interaction, select: discord.ui.Select
    ):
        self.selected_field = select.values[0]
        if self.selected_field == "fetch entire entry":
            self.selected_field = None
        return await interaction.response.defer()

    @discord.ui.button(label="Submit", style=discord.ButtonStyle.gray, row=4)
    async def fetch_entry_button_submit(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        user_id = interaction.user.id
        if not (self.selected_entry and self.selected_language):
            await interaction.response.send_message(
                f"<@{user_id}> Please make sure you have chosen an entry and language!",
                ephemeral=True,  # only the user who called it can see this msg
            )
            return
        return await _fetch_entry_with_json(
            interaction,
            int(self.selected_entry),
            self.selected_language,
            self.selected_field,
        )


def register_commands(tree, this_guild: discord.Object):
    @tree.command(
        name="ui-fetch",
        description="Eady-to-use entry selector",
        guild=this_guild,
    )
    async def ui_fetch(interaction: discord.Interaction):
        button = FetchEntryView()
        await interaction.response.send_message(
            "What would you like to see?", view=button
        )
