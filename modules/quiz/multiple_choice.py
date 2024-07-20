import discord

class QuizMultipleChoiceButton(discord.ui.Button["MultipleChoiceButton"]):
    def __init__(self, x: int, y: int, label: str, is_correct: bool):
        super().__init__(
            style=discord.ButtonStyle.secondary, # need to change this?
            label=label,
            row=y
        )
        self.x = x
        self.y = y
        self.label = label
        self.is_correct = is_correct

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None, "View not found"
        view: MultipleChoiceButton = self.view
        # if correct, change style to green and disable all buttons
        if self.is_correct:
            self.style = discord.ButtonStyle.success
            for child in view.children:
                child.disabled = True
        # if incorrect, change style to red and disable this button
        else:
            self.style = discord.ButtonStyle.danger
            self.disabled = True
        await interaction.response.edit_message(view=view)

class MultipleChoiceButton(discord.ui.View):
    def __init__(self, choices: list[QuizChoice]):
        super().__init__()

class QuizChoice:
    def __init__(self, label: str, is_correct: bool):
        self.label = label
        self.is_correct = is_correct