import discord


class ButtonView(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.gray)
    async def hgs_button_yes(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.send_message("Correct")

    @discord.ui.button(label="No", style=discord.ButtonStyle.gray)
    async def hgs_button_no(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.send_message(
            "Your opinion has been ignored"
        )


def register_commands(tree, this_guild: discord.Object):
    @tree.command(
        name="hgs",
        description="The ultimate question",
        guild=this_guild,
    )
    async def hgs(interaction: discord.Interaction):
        button = ButtonView()
        await interaction.response.send_message("Hot gay sex?", view=button)
