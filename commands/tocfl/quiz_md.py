import discord
from discord.app_commands import Choice
import sys, re, random
from pathlib import Path
import pandas as pd

sys.path.append(str(Path(__file__).parent.parent.parent))  # I hate python imports
from modules.quiz.multiple_choice import MultipleChoiceView, QuizChoice
from .read_naer_MD_csv import NAER_MD_CSV

DISCORD_MAX_LABEL_LENGTH = 80
NUM_ROWS_CHOICES = [Choice(name=i, value=i) for i in range(2, 5 + 1)]  # multiple choice options are from 2 to 5

# Quiz specifics:
# - Subject: Choose the correct Mandarin translation for the English word
# - Choice: Mandarin translation
class NAER_MD_QuizChoice(QuizChoice):
    def __init__(self, is_correct: bool, mandarin: str = ""):
        label = mandarin # could probably add more stuff here in the future
        if len(label) > DISCORD_MAX_LABEL_LENGTH:
            # discord only allows 80 characters for the label, so truncate if necessary
            label = label[:DISCORD_MAX_LABEL_LENGTH]
            # replace the last three characters with an ellipsis
            label = label[:-3] + "..."
        super().__init__(label, is_correct)

def get_n_random_rows(df: pd.DataFrame, n: int) -> pd.DataFrame:
    # get n random UNIQUE rows based on "md" column, since that column has duplicates (EN doesn't)
    words = df["md"].drop_duplicates().sample(n)
    # select all rows that have the selected mandarin words (possibly more than n rows)
    rows = df[df["md"].isin(words)]
    # shuffle the rows then drop duplicates based on "word" column, so we have exactly n rows that are randomly selected
    # .sample(frac=1) shuffles the rows, i.e. return all (1.0x) rows in random order
    return rows.sample(frac=1).drop_duplicates(subset=["md"])
    

def register_MD_quiz_subcommand(
    tocfl_group: discord.app_commands.Group,
):
    @tocfl_group.command(
        name="quiz-mandarin",
        description="Guess the Mandarin translation of the English word",
    )
    @discord.app_commands.describe(is_private="Whether the quiz should be private")
    @discord.app_commands.choices(num_rows=NUM_ROWS_CHOICES)
    async def naer_quiz(
        interaction: discord.Interaction,
        num_rows: Choice[int] = None,
        is_private: bool = False,
    ):
        # get num_rows random rows and choose one as the correct answer
        random_rows = get_n_random_rows(NAER_MD_CSV, num_rows.value if num_rows else 4)
        correct_row_index = random_rows.sample().index[0]
        correct_row = random_rows.loc[correct_row_index]
        # convert to NAER_MD_QuizChoice objects
        choices = [
            NAER_MD_QuizChoice(correct_row_index == i, row["md"])
            for i, row in random_rows.iterrows()
        ]
        # shuffle the choices
        random.shuffle(choices)
        # create the multiple choice view
        view = MultipleChoiceView(choices)
        # create the prompt
        prompt = f"Choose the correct Mandarin meaning of the English word: \n# {correct_row['en']}"
        # send the message
        await interaction.response.send_message(
            prompt,
            view=view,
            ephemeral=is_private,
        )

if __name__ == "__main__":
    random_rows = get_n_random_rows(NAER_MD_CSV, 4)
    print(random_rows)