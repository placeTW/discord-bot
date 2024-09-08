import string
import discord
from discord import app_commands

from bot import TWPlaceClient
from modules.supabase import supabaseClient
from random import randint
from .consts import TOCFL_LEVELS_CHOICES, TOCFL_LEVELS
from .chewing import to_chewing
from .quiz_vocab import register_vocab_quiz_subcommand


def register_commands(
    tree: discord.app_commands.CommandTree,
    this_guild: discord.Object,
    client: discord.Client,
):
    tocfl_group = app_commands.Group(name="tocfl", description="TOCFL commands")

    register_vocab_quiz_subcommand(tocfl_group)

    @tocfl_group.command(
        name="random",
        description="Get a random TOCFL word",
    )
    @app_commands.choices(level=TOCFL_LEVELS_CHOICES)
    @app_commands.describe(level="The level of the word to get")
    async def tocfl_rand(
        interaction: discord.Interaction,
        level: discord.app_commands.Choice[int] = None,
    ):
        MAX_ID = 7563  # fixed for now until we can get the max id from the db
        random_id = randint(1, MAX_ID)
        tocfl_table = supabaseClient.table("tocfl")
        data, count = (
            supabaseClient.rpc('get_random_tocfl', {'level': level.value}).execute()
            if level
            else tocfl_table.select("*").eq("id", random_id).execute()
        )
        if count == 0:
            await interaction.response.send_message(
                f"There was an error getting the random word. Please try again",
                ephemeral=True,
            )
            return
        data = data[1]  # the first element is just the string "data"
        data = data[0]  # rand only has one element
        # example data: {'id': 112, 'vocab': '找', 'zhuyin': None, 'pinyin': 'zhăo ', 'english': None, 'level': 1, 'part_of_speech': 'V', 'context': '與他人的關係'}
        embed = _create_word_embed(
            data["vocab"],
            TOCFL_LEVELS[data["level"]],
            data["part_of_speech"],
            data["pinyin"],
        )
        await interaction.response.send_message(f"Random word from TOCFL word list:", embed=embed)

    tree.add_command(tocfl_group, guild=this_guild)


def _create_word_embed(word: str, level: int, part_of_speech: str, pinyin: str):
    try:
        chewing = to_chewing(pinyin)
    except AssertionError as e:
        print("Error occurred during chewing conversion: ", e)
        chewing = None

    embed = discord.Embed(title=word)  # ^ add description="desc" for translation
    embed.add_field(name="Pronunciation (Pinyin)", value=pinyin, inline=False)
    if chewing:
        embed.add_field(name="Pronunciation (Zhuyin)", value=chewing, inline=False)
    embed.add_field(
        name="Dictionary Reference",
        value=f"https://cdict.net/?q={word}",
        inline=False,
    )
    embed.add_field(name="Level", value=level, inline=False)
    if part_of_speech:
        embed.add_field(name="Grammar Category", value=part_of_speech, inline=False)
    # stroke order
    embed.add_field(name="Stroke Order", value="", inline=False)
    for character in word.translate(str.maketrans('', '', string.punctuation)):
        embed.add_field(
            name="",
            value=f"[Stroke order for {character}](https://stroke-order.learningweb.moe.edu.tw/charactersQueryResult.do?words={character}&lang=zh_TW&csrfPreventionSalt=null)",
            inline=False,
        )

    # embed.set_footer(
    #     text="Source: https://tocfl.edu.tw/index.php/exam/download"
    # )
    return embed
