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


class SubmitEntryModal(discord.ui.Modal):
    def __init__(
        self,
        client: discord.Client,
        form_title: str,
        lang: str,
        entry_id: int,
        entry_name: str,
        field: str,
        *,
        timeout: float = None,
    ) -> None:
        super().__init__(title=form_title, timeout=timeout)
        self.the_client = client
        self.approval_channel = client.get_channel(WAITING_APPROVAL_CHANNEL_ID)
        self.proposed_entry = discord.ui.TextInput(
            label=f"Add your new entry here",
            style=discord.TextStyle.paragraph,
            min_length=1,
            placeholder=f"Add your new text here.\nEntry: {entry_name} Language: {lang} Field: {field}",
        )
        self.add_item(self.proposed_entry)

        # save relevant vars
        self.lang = lang
        self.entry_id = entry_id
        self.entry_name = entry_name
        self.field = field

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Thanks for your response! The team will review your request soon.",
            ephemeral=True,
        )
        user_name = interaction.user.name
        user_id = interaction.user.id
        approve_deny_view = ApproveDenyTranslationEntryView(
            self,
            self.lang,
            self.entry_id,
            self.entry_name,
            self.field,
            user_id,
            # self.proposed_entry.value,
            interaction.channel_id,
        )
        self.sent_msg = await self.approval_channel.send(
            f"User {user_name} has proposed a change for this entry:\n"
            + f"* Entry: {self.entry_name} \n"
            + f"* Language: {self.lang} \n"
            + f"* Field: {self.field} \n"
            + f"* The proposed change is: \n"
            + f"`{self.proposed_entry.value}`",
            view=approve_deny_view,
            silent=True,
        )

        # approve_deny_view.set_msg_id(sent_msg.id)


class ApproveDenyTranslationEntryView(discord.ui.View):
    def __init__(  # we need this extra info to create PR
        self,
        the_modal: SubmitEntryModal,
        lang: str,
        entry_id: int,
        entry_name: str,
        field: str,
        proposing_user_id: int,
        proposed_text: str,
        # proposed_channel_id: int,
        year: int = 2023,
    ):
        super().__init__()
        self.the_modal = the_modal

    def set_msg_id(self, msg_id: int):
        self.msg_id = msg_id
        print(f"msg id: {msg_id}")

    async def disable_buttons(self):
        for button in self.children:
            button.disabled = True
        await self.the_modal.sent_msg.edit(view=self)

    @discord.ui.button(label="Approve", style=discord.ButtonStyle.green)
    async def edit_entry_button_approve(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await self.disable_buttons()
        await interaction.response.send_message("Approved change!")

    @discord.ui.button(label="Deny", style=discord.ButtonStyle.red)
    async def edit_entry_button_deny(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await self.disable_buttons(interaction)
        await interaction.response.send_message("Denied change!")


if __name__ == "__main__":
    import asyncio

    link = "https://placetw.com/locales/en/art-pieces.json"
    asyncio.run(async_utils._async_get_json(link))
