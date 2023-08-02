import discord
from ..github_pullrequest import modify_json_and_create_pull_request
import tempfile, json
import os
import stat

# channel to receive approval requests
WAITING_APPROVAL_CHANNEL_ID = 1135991380242608259


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
            placeholder=f"Add your new text here.\n"
            # + f"Entry: {entry_name} Language: {lang} Field: {field}\n",
            + f"For links, separate all links with commas.",
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
        submitted_msg = await interaction.original_response()
        user_name = interaction.user.name
        user_id = interaction.user.id
        proposed_channel = self.the_client.get_channel(interaction.channel_id)
        approve_deny_view = ApproveDenyTranslationEntryView(
            the_modal=self,
            lang=self.lang,
            entry_id=self.entry_id,
            entry_name=self.entry_name,
            field=self.field,
            proposing_user_id=user_id,
            proposed_text=self.proposed_entry.value,
            proposed_channel=proposed_channel,
            approval_channel=self.approval_channel,
        )
        self.sent_msg = await self.approval_channel.send(
            f"User {user_name} has proposed a change for this entry:\n"
            + f"* Entry: {self.entry_name} \n"
            + f"* Language: {self.lang} \n"
            + f"* Field: {self.field} \n"
            + f"* The proposed change is: \n"
            + f"`{self.proposed_entry.value}`",
            view=approve_deny_view,
        )


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
        proposed_channel: discord.TextChannel,
        approval_channel: discord.TextChannel,
        year: int = 2023,
    ):
        super().__init__(timeout=None)
        self.the_modal = the_modal
        self.proposed_channel = proposed_channel
        self.proposing_user_id = proposing_user_id
        self.lang = lang
        self.entry_id = entry_id
        self.entry_name = entry_name
        self.field = field
        self.proposed_text = proposed_text
        self.approval_channel = approval_channel

    async def disable_buttons(self):
        for button in self.children:
            button.disabled = True
        self.stop()
        await self.the_modal.sent_msg.edit(view=self)

    @discord.ui.button(label="Approve", style=discord.ButtonStyle.green)
    async def edit_entry_button_approve(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await self.disable_buttons()
        await interaction.response.send_message("Approved change!")
        await self.proposed_channel.send(
            f"<@{self.proposing_user_id}>' submission has been accepted!"
            + " Expect to see the changes soon. 🎉"
        )

        resulting_json = await modify_json_and_create_pull_request(
            self.lang,
            self.entry_id,
            self.entry_name,
            self.field,
            self.proposed_text,
        )

        # create temporary file
        temporary_file = tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", delete=False, dir=".", suffix=".json"
        )
        tempfilename = temporary_file.name
        os.chmod(tempfilename, 777)
        json.dump(resulting_json, temporary_file, ensure_ascii=False, indent=2)
        temporary_file.flush()
        temporary_file.close()

        temporary_file_again = open(tempfilename, "rb")
        file_to_send = discord.File(
            temporary_file_again, filename="user_proposal.json"
        )
        # upload file so mods can see
        await self.approval_channel.send(
            "User's proposed changes:",
            reference=self.the_modal.sent_msg,
            file=file_to_send,
        )
        temporary_file_again.close()
        # delete the temp file afterwards
        os.chmod(tempfilename, stat.S_IWRITE)
        os.unlink(tempfilename)

    @discord.ui.button(label="Deny", style=discord.ButtonStyle.red)
    async def edit_entry_button_deny(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await self.disable_buttons()
        await interaction.response.send_message("Denied change!")
        # await self.proposed_channel.send(
        #     "Unfortunately, your submission entry has been denied. "
        #     + "Please let us know if you have questions."
        # )
