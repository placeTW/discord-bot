import discord
from typing import List, Tuple
import pandas as pd
from random import shuffle
from .chewing import PINYIN_INITIALS, PINYIN_CENTER, PINYIN_FINALS


from modules.quiz.multiple_choice import MultipleChoiceView, QuizChoice
from discord.app_commands import Choice

NUM_ROWS_CHOICES = [Choice(name=i, value=i) for i in range(2, 5 + 1)]  # multiple choice options are from 2 to 5


def _get_random_bopomofo_pinyin_from_dict(num_choices: int = 4) -> List[dict]:
    full_dict = PINYIN_INITIALS | PINYIN_CENTER | PINYIN_FINALS
    # get num_choices random choices from the dictionary: turn dict into list of tuples, shuffle, and slice the first num_choices
    full_list = list(full_dict.items())
    shuffle(full_list)
    return full_list[:num_choices] # sample output: [('p', 'ㄆ'), ('er', 'ㄦ'), ('i', 'ㄧ'), ('d', 'ㄉ')]

def _bopomofo_dict_to_choices(bopomofo_pinyin_list: List[dict], label="bopomofo") -> Tuple[List[QuizChoice], str]:
    assert label in ("bopomofo", "pinyin"), "label must be either 'bopomofo' or 'pinyin'"
    label_index = 0 if label == "bopomofo" else 1
    question_index = (label_index + 1) % 2
    # choose the first element as the correct answer
    correct_index = 0
    correct_choice = QuizChoice(bopomofo_pinyin_list[correct_index][question_index], is_correct=True)
    text_to_display = bopomofo_pinyin_list[correct_index][label_index]
    wrong_choices = [QuizChoice(pair[question_index], is_correct=False) for pair in bopomofo_pinyin_list[1:]]
    choices = [correct_choice] + wrong_choices
    shuffle(choices)
    return choices, text_to_display

def register_bopomofo_quiz_subcommand(
    tocfl_group: discord.app_commands.Group,
):
    @tocfl_group.command(
        name="quiz-bopomofo",
        description="Guess the Bopomofo of the given Pinyin",
    )
    @discord.app_commands.describe(is_private="Whether the quiz should be private")
    @discord.app_commands.choices(num_rows=NUM_ROWS_CHOICES)
    async def tocfl_quiz_pronunciation(
        interaction: discord.Interaction,
        num_rows: Choice[int] = 4,
        is_private: bool = False,
    ):
        num_rows = num_rows.value if isinstance(num_rows, Choice) else num_rows
        # get random choices from the dictionary
        choices, text_to_display = _bopomofo_dict_to_choices(_get_random_bopomofo_pinyin_from_dict(num_rows), label="bopomofo")
        view = MultipleChoiceView(choices)
        await interaction.response.send_message(
            f"Choose the Bopomofo of the given Pinyin: {text_to_display}",
            view=view,
            ephemeral=is_private,
        )

    @tocfl_group.command(
        name="quiz-pinyin",
        description="Guess the Pinyin of the given Bopomofo",
    )
    @discord.app_commands.describe(is_private="Whether the quiz should be private")
    @discord.app_commands.choices(num_rows=NUM_ROWS_CHOICES)
    @discord.app_commands.rename(num_rows="number-of-choices")
    @discord.app_commands.rename(is_private="make-quiz-private")
    async def tocfl_quiz_pronunciation(
        interaction: discord.Interaction,
        num_rows: Choice[int] = 4,
        is_private: bool = False,
    ):
        num_rows = num_rows.value if isinstance(num_rows, Choice) else num_rows
        # get random choices from the dictionary
        choices, text_to_display = _bopomofo_dict_to_choices(_get_random_bopomofo_pinyin_from_dict(num_rows), label="pinyin")
        view = MultipleChoiceView(choices)
        await interaction.response.send_message(
            f"Choose the Pinyin of the given Bopomofo: {text_to_display}",
            view=view,
            ephemeral=is_private,
        )



if __name__ == "__main__":
    num_choices = 4
    choices, text_to_display = _bopomofo_dict_to_choices(_get_random_bopomofo_pinyin_from_dict(num_choices), label="pinyin")
    print("Choices:", choices)
    print("Text to display:", text_to_display)