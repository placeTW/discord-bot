import discord
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent)) # I hate python imports
from modules.quiz.multiple_choice import MultipleChoiceView, QuizChoice
from .read_embree_csv import TW_EMBREE_CSV

class TaigiQuizChoice(QuizChoice):
    def __init__(self, poj_unicode: str, is_correct: bool, engbun:str="", hoabun:str=""):
        label = f"{engbun}" + f" ({hoabun})" if hoabun else ""
        super().__init__(label, is_correct)

def register_quiz_subcommand(
    taigi_group: discord.app_commands.Group,
):
    @taigi_group.command(
        name="quiz",
        description="Start a quiz (multiple choice) on Taiwanese words",
    )
    async def taigi_quiz(
        interaction: discord.Interaction,
        is_private: bool = False,
    ):
        # get four random rows and choose one as the correct answer
        random_rows = TW_EMBREE_CSV.sample(4)
        # convert to TaigiQuizChoice objects
        correct_row_index = random_rows.sample().index[0]
        choices = [
            TaigiQuizChoice(row["PojUnicode"], correct_row_index == i, row["EngBun"], row["HoaBun"])
            for i, row in random_rows.iterrows()
        ]
        # create the view
        view = MultipleChoiceView(choices)
        # send the message
        await interaction.response.send_message(
            f"Choose the correct meaning of the Taiwanese word: {random_rows.loc[correct_row_index, 'PojUnicode']}",
            view=view,
        )