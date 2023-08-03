import discord


class HGSButtonView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)  # keep alive for 60 seconds
        self.msg: discord.Message = None

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green)
    async def hgs_button_yes(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        user_id = interaction.user.id
        await interaction.response.send_message(f"<@{user_id}> is correct")

    @discord.ui.button(label="No", style=discord.ButtonStyle.blurple)
    async def hgs_button_no(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        user_id = interaction.user.id
        await interaction.response.send_message(
            f"<@{user_id}>'s opinion has been ignored"
        )

    async def on_timeout(self) -> None:
        """Delete message upon timeout."""
        await self.msg.delete()


def register_commands(tree, this_guild: discord.Object):
    @tree.command(
        name="hgs",
        description="The ultimate question",
        guild=this_guild,
    )
    async def hgs(interaction: discord.Interaction):
        button = HGSButtonView()

        await interaction.response.send_message("Hot gay sex?", view=button)
        button.msg = await interaction.original_response()
