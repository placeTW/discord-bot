import asyncio
import discord
from discord import app_commands
from ..modules import async_utils, postprocess
import typing
from discord.app_commands import Choice

from .consts import (
    SUPPORTED_LANGUAGE_CODES,
    SUPPORTED_ART_FIELDS,
    SUPPORTED_ART2023_IDS,
    POSSIBLE_ART2023_IDS,
)


class FetchEntryView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.selected_language = None

    # * There should be fields for:
    # * - lang (drop down menu)
    # * - field (drop down menu)
    # * - year (drop down menu, only has 2023 atm)
    # * - submit (button)

    @discord.ui.select(
        placeholder="Choose an entry",
        options=[
            discord.SelectOption(label=entry_id, description=entry_desc)
            for entry_id, entry_desc in SUPPORTED_ART2023_IDS.items()
        ],
        row=1,
    )
    async def select_callback(self, interaction: discord.Interaction, select):
        self.selected_language = select.values[0]
        return await interaction.response.defer()

    # @discord.ui.select(
    #     placeholder="Choose a language",
    #     options=[
    #         discord.SelectOption(label=entry_id, description="desc")
    #         for entry_id in SUPPORTED_ART2023_IDS
    #     ],
    #     row=2,
    # )
    # async def select_callback(self, interaction: discord.Interaction, select):
    #     self.selected_language = select.values[0]
    #     return await interaction.response.defer()

    @discord.ui.button(label="Submit", style=discord.ButtonStyle.gray, row=3)
    async def hgs_button_submit(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        user_id = interaction.user.id

        await interaction.response.send_message(
            f"<@{user_id}> Your results:\n* \
                chosen entry: {self.selected_language}"
        )


def register_commands(tree, this_guild: discord.Object):
    @tree.command(
        name="ui-fetch",
        description="Eady-to-use entry selector",
        guild=this_guild,
    )
    async def hgs(interaction: discord.Interaction):
        button = FetchEntryView()
        await interaction.response.send_message(
            "What would you like to see?", view=button
        )
