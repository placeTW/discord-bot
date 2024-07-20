import discord
from ..modules.quiz.multiple_choice import MultipleChoiceView, QuizChoice

class TaigiQuizChoice(QuizChoice):
    def __init__(self, poj_unicode: str, is_correct: bool, engbun:str="", hoabun:str=""):
        super().__init__(poj_unicode, is_correct)
        self.engbun = engbun
        self.hoabun = hoabun

def register_subcommand(
    taigi_group: discord.app_commands.Group,
):
    @taigi_group.command(
        name="quiz",
        description="Start a quiz (multiple choice) on Taiwanese words",
    )
    async def taigi_quiz(
        interaction: discord.Interaction,
    ):
        # get four random rows and choose one as the correct answer
        random_rows = TW_EMBREE_CSV.sample(4)
        # convert to TaigiQuizChoice objects
        choices = [
            TaigiQuizChoice(row["PojUnicode"], row["IsCorrect"], row["EngBun"], row["HoaBun"])
            for _, row in random_rows.iterrows()
        ]
        correct_row_index = random_rows.sample().index[0]
