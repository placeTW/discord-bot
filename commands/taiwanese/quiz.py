import discord
from discord.app_commands import Choice
import sys, re, random
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent)) # I hate python imports
from modules.quiz.multiple_choice import MultipleChoiceView, QuizChoice
from .read_embree_csv import TW_EMBREE_CSV, NUM_WORDS_COL

DISCORD_MAX_LABEL_LENGTH = 80

class TaigiQuizChoice(QuizChoice):
    def __init__(self, poj_unicode: str, is_correct: bool, engbun:str="", hoabun:str=""):
        engbun = re.sub(r"<.*?>", "", engbun) # remove explanation in engbun, which is denoted by <>, since it might contain the answer
        label = f"{engbun}" + f" ({hoabun})" if hoabun else ""
        if len(label) > DISCORD_MAX_LABEL_LENGTH:
            # discord only allows 80 characters for the label, so truncate if necessary
            label = label[:DISCORD_MAX_LABEL_LENGTH]
            # replace the last three characters with an ellipsis
            label = label[:-3] + "..."
        super().__init__(label, is_correct)

NUM_ROWS_CHOICES = [Choice(name=i, value=i) for i in range(2, 5+1)] # multiple choice options are from 2 to 5

def register_quiz_subcommand(
    taigi_group: discord.app_commands.Group,
):
    @taigi_group.command(
        name="quiz",
        description="Start a quiz (multiple choice) on Taiwanese words",
    )
    @discord.app_commands.describe(is_private="Whether the quiz should be private")
    @discord.app_commands.choices(num_rows=NUM_ROWS_CHOICES)
    async def taigi_quiz(
        interaction: discord.Interaction,
        num_rows: Choice[int] = None,
        is_private: bool = False,
    ):
        # select a random value from the NUM_WORDS_COL column
        word_length = TW_EMBREE_CSV[NUM_WORDS_COL].sample().iloc[0]
        # filter the dataframe based on the word length
        tw_csv_subset = TW_EMBREE_CSV[TW_EMBREE_CSV[NUM_WORDS_COL] == word_length]
        # get the number of rows to sample, which is the minimum of 4 and the length of the subset
        num_rows = min(num_rows.value if num_rows else 4, len(tw_csv_subset))
        # get num_rows random rows and choose one as the correct answer
        random_rows = tw_csv_subset.sample(num_rows)
        # convert to TaigiQuizChoice objects
        correct_row_index = random_rows.sample().index[0]
        choices = [
            TaigiQuizChoice(row["PojUnicode"], correct_row_index == i, row["EngBun"], row["HoaBun"])
            for i, row in random_rows.iterrows()
        ]
        # shuffle the choices
        random.shuffle(choices)
        # create the view
        view = MultipleChoiceView(choices)
        # send the message
        await interaction.response.send_message(
            f"Choose the correct meaning of the Taiwanese word: \n# {random_rows.loc[correct_row_index, 'PojUnicode']}",
            view=view,
            ephemeral=is_private,
        )