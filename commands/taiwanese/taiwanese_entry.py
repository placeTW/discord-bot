import pandas as pd
from pathlib import Path
import discord
from discord import app_commands
from .read_embree_csv import read_embree_csv_raw
from urllib.parse import quote as url_quote
from .quiz import register_quiz_subcommand
from .read_embree_csv import TW_EMBREE_CSV


def get_random_row(df: pd.DataFrame) -> pd.Series:
    return df.sample().iloc[0]


def register_commands(
    tree: discord.app_commands.CommandTree,
    this_guild: discord.Object,
    client: discord.Client,
):
    taigi_group = app_commands.Group(name="taigi", description="Taiwanese commands")

    @taigi_group.command(
        name="random",
        description="Get a random Taiwanese word",
    )
    async def taigi_rand(
        interaction: discord.Interaction,
    ):
        random_row = get_random_row(TW_EMBREE_CSV)
        embed = _create_word_embed(
            random_row["PojUnicode"],
            random_row["PojInput"],
            random_row["Abbreviation"],
            random_row["NounClassifier"],
            random_row["HoaBun"],
            random_row["EngBun"],
        )
        await interaction.response.send_message(f"Random word from Taiwanese word list:", embed=embed)

    # register the quiz subcommand
    register_quiz_subcommand(taigi_group)

    tree.add_command(taigi_group, guild=this_guild)


def _create_word_embed(
    poj_unicode: str,
    poj_input: str,
    abbreviation: str,
    noun_classifier: str,
    hoa_bun: str,
    eng_bun: str,
):
    embed = discord.Embed(
        title=poj_unicode, color=discord.Color.green()
    )  # ^ add description="desc" for additional info
    # escape the unicode for the URL
    poj_unicode = url_quote(poj_unicode)
    poj_input = url_quote(poj_input)
    embed.add_field(name="Mandarin equivalent", value=hoa_bun, inline=False)
    embed.add_field(name="English meaning", value=eng_bun, inline=False)
    embed.add_field(name="POJ input", value=poj_input, inline=False)
    if abbreviation:
        embed.add_field(name="Word Type", value=abbreviation, inline=False)
    if noun_classifier:
        embed.add_field(name="Noun classifier", value=noun_classifier, inline=False)
    chhoe_taigi_link = (
        f"https://chhoe.taigi.info/search?method=basic&searchMethod=equals&spelling={poj_input}&spellingMethod=PojInput"
    )
    itaigi_link = f"https://itaigi.tw/k/{hoa_bun}/"
    moe_link_definition = f"https://sutian.moe.edu.tw/zh-hant/tshiau/?lui=tai_su&tsha={poj_unicode}"  # ! might need to use the official MOE unicode from the df
    moe_link_examples = f"https://sutian.moe.edu.tw/zh-hant/tshiau/?lui=tai_ku&tsha={poj_unicode}"
    embed.add_field(name="Links", value="", inline=False)
    embed.add_field(name=f"", value=f"[Itaigi Search (Pronunciation)]({itaigi_link})", inline=False)
    embed.add_field(name=f"", value=f"[MOE Dictionary (Definition)]({moe_link_definition})", inline=False)
    embed.add_field(name=f"", value=f"[MOE Dictionary (Examples)]({moe_link_examples})", inline=False)
    embed.add_field(name=f"", value=f"[ChhoeTaigi Search (Source)]({chhoe_taigi_link})", inline=False)
    # general Taiwanese pronunciation resources
    embed.add_field(name="台羅 Pronunciation Guides (in Mandarin)", value="", inline=False)
    embed.add_field(name=f"", value=f"[一個禮拜學好台羅拼音！](https://hackmd.io/@itk1523/1week-kip)", inline=False)
    embed.add_field(name=f"", value=f"[教育部台羅教學網](https://tailo.moe.edu.tw/)", inline=False)

    # embed.set_footer(text="Data from ChhoeTaigi", icon_url="https://chhoe.taigi.info/favicon-light.ico") # not used because there's no suitable icon atm
    return embed
