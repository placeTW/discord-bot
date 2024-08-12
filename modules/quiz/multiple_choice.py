import discord


class QuizMultipleChoiceButton(discord.ui.Button["MultipleChoiceButton"]):
    def __init__(self, x: int, y: int, label: str, is_correct: bool):
        super().__init__(style=discord.ButtonStyle.secondary, label=label, row=x)  # need to change this?
        self.x = x
        self.y = y
        self.label = label
        self.is_correct = is_correct

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None, "View not found"
        view: MultipleChoiceView = self.view
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


# a generic class for a multiple choice question
class QuizChoice:
    def __init__(self, label: str, is_correct: bool):
        self.label = label
        self.is_correct = is_correct


class MultipleChoiceView(discord.ui.View):
    def __init__(self, choices: list[QuizChoice], timeout: int = 300):
        super().__init__(timeout=timeout)
        for i, choice in enumerate(choices):
            self.add_item(QuizMultipleChoiceButton(i, 0, choice.label, choice.is_correct))
