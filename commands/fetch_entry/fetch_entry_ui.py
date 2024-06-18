import asyncio
import discord
from discord import app_commands
from modules import async_utils, postprocess
import typing
from discord.app_commands import Choice
from .fetch_entry_main import _fetch_entry_with_json, send_fetch_response

from ..entry_consts.consts import (
    SUPPORTED_ART2023_IDS,
    POSSIBLE_ART2023_IDS,
    SUPPORTED_ART_FIELDS,
    POSSIBLE_LANGUAGE_CODES,
    SUPPORTED_LANGUAGE_CODES,
)


# for views tutorial: see
class FetchEntryView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=180)
        # these are for storing the user's choices
        self.selected_entry = None
        self.selected_language = None
        self.selected_field = None
        self.msg: discord.Message = None  # associated msg

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
                label=entry_desc, description=entry_id, value=entry_id
            )
            for entry_id, entry_desc in SUPPORTED_ART2023_IDS.items()
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
            discord.SelectOption(
                label=lang_name, description=lang_id, value=lang_id
            )
            for lang_id, lang_name in SUPPORTED_LANGUAGE_CODES.items()
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
            discord.SelectOption(
                label=field_desc, description=field_id, value=field_id
            )
            for field_id, field_desc in (
                SUPPORTED_ART_FIELDS
                | {"fetch_entire_entry": "Fetch entire entry"}
            ).items()
        ],
        row=3,
    )
    async def select_field_callback(
        self, interaction: discord.Interaction, select: discord.ui.Select
    ):
        self.selected_field = select.values[0]
        if self.selected_field == "fetch_entire_entry":
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
        result = await _fetch_entry_with_json(
            interaction,
            self.selected_entry,
            self.selected_language,
            self.selected_field,
        )
        await send_fetch_response(
            interaction,
            result,
            self.selected_entry,
            self.selected_language,
            self.selected_field,
        )

    async def on_timeout(self) -> None:
        button = self.children[-1]
        self.remove_item(button)
        for child in self.children:
            child.disabled = True
        await self.msg.edit(
            content="This widget is no longer usable due to inactivity.\n"
            + "You can also run the command yourself by typing `/ui-fetch` in chat.",
            view=self,
        )


def register_commands(tree, guilds: list[discord.Object]):
    @tree.command(
        name="ui-fetch",
        description="Eady-to-use entry selector",
        guilds=guilds,
    )
    async def ui_fetch(interaction: discord.Interaction):
        button = FetchEntryView()
        await interaction.response.send_message(
            "What would you like to see?", view=button
        )
        button.msg = await interaction.original_response()
