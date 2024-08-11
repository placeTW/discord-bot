from .db import get_random_tocfl_choices_from_db
import discord
from typing import List, Tuple
import pandas as pd
from random import shuffle
from .chewing import to_chewing

# sys.path.append(str(Path(__file__).parent.parent.parent)) # I hate python imports
from modules.quiz.multiple_choice import MultipleChoiceView, QuizChoice
from discord.app_commands import Choice

NUM_ROWS_CHOICES = [Choice(name=i, value=i) for i in range(2, 5 + 1)]  # multiple choice options are from 2 to 5


def _db_results_to_df(results: List[dict]) -> pd.DataFrame:
    df = pd.DataFrame(results)
    # for "vocab" and "pinyin" columns: only keep the first part of the string
    df["vocab"] = df["vocab"].apply(lambda x: x.split("/")[0])
    df["pinyin"] = df["pinyin"].apply(lambda x: x.split("/")[0])
    # add zhuyin column
    try:
        df["zhuyin"] = (
            df["pinyin"].apply(to_chewing).str.replace("\u3000", " ")
        )  # replace full-width space with half-width space for now
        # add "pronunciation" column as a combination of pinyin and zhuyin
        df["pronunciation"] = df["pinyin"] + " / " + df["zhuyin"]
        # drop the "pinyin" and "zhuyin" columns
        df.drop(columns=["pinyin", "zhuyin"], inplace=True)
    except Exception as e:
        df["pronunciation"] = df["pinyin"]
        df.drop(columns=["pinyin"], inplace=True)
    return df.set_index("id")


def df_results_to_choices(
    df: pd.DataFrame, num_choices: int, is_ask_pronunciation: bool = True
) -> Tuple[List[QuizChoice], str]:
    col_to_display, col_to_ask = ("pronunciation", "vocab") if is_ask_pronunciation else ("vocab", "pronunciation")
    # select one row as the correct answer
    correct_row_index = df.sample().index[0]
    vocab_to_display = df.loc[correct_row_index, col_to_ask]
    # convert to QuizChoice object
    correct_choice = QuizChoice(df.loc[correct_row_index, col_to_display], is_correct=True)
    # select incorrect choices as rows that do not have the same pronunciation as the correct answer
    incorrect_rows = df[df[col_to_display] != correct_choice.label].sample(num_choices - 1)
    incorrect_choices = [QuizChoice(row[col_to_display], is_correct=False) for _, row in incorrect_rows.iterrows()]
    # shuffle the choices
    choices = [correct_choice] + incorrect_choices
    shuffle(choices)
    return choices, vocab_to_display


def register_quiz_subcommand(
    tocfl_group: discord.app_commands.Group,
):
    @tocfl_group.command(
        name="quiz-pronunciation",
        description="Guess the pronunciation of the given TOCFL word",
    )
    @discord.app_commands.describe(is_private="Whether the quiz should be private")
    @discord.app_commands.choices(num_rows=NUM_ROWS_CHOICES)
    async def tocfl_quiz_pronunciation(
        interaction: discord.Interaction,
        num_rows: Choice[int] = 4,
        is_private: bool = False,
    ):
        # get random choices from the database
        choices = get_random_tocfl_choices_from_db(num_choices=num_rows)
        # convert to DataFrame
        df = _db_results_to_df(choices)
        # convert to QuizChoice objects
        choices, vocab_to_ask = df_results_to_choices(df, num_rows, is_ask_pronunciation=True)
        # create the view
        view = MultipleChoiceView(choices=choices)
        # send the message
        await interaction.response.send_message(
            f"Choose the correct pronunciation for: {vocab_to_ask}",
            view=view,
            ephemeral=is_private,
        )

    @tocfl_group.command(
        name="quiz-vocab",
        description="Guess the character of the given TOCFL pronunciation",
    )
    @discord.app_commands.describe(is_private="Whether the quiz should be private")
    @discord.app_commands.choices(num_rows=NUM_ROWS_CHOICES)
    async def tocfl_quiz_vocab(
        interaction: discord.Interaction,
        num_rows: Choice[int] = 4,
        is_private: bool = False,
    ):
        # get random choices from the database
        choices = get_random_tocfl_choices_from_db(num_choices=num_rows)
        # convert to DataFrame
        df = _db_results_to_df(choices)
        # convert to QuizChoice objects
        choices, vocab_to_ask = df_results_to_choices(df, num_rows, is_ask_pronunciation=False)
        # create the view
        view = MultipleChoiceView(choices=choices)
        # send the message
        await interaction.response.send_message(
            f"Choose the correct answer for: {vocab_to_ask}",
            view=view,
            ephemeral=is_private,
        )


if __name__ == "__main__":
    num_choices = 4
    choices = get_random_tocfl_choices_from_db(num_choices=num_choices)
    df = _db_results_to_df(choices)
    choices, vocab_to_ask = df_results_to_choices(df, num_choices, is_ask_pronunciation=False)
    print(f"Choose the correct answer for: {vocab_to_ask}")
    print("Choices:")
    print('\n'.join(['* ' + choice.label for choice in choices]))
