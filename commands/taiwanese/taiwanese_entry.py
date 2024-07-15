import pandas as pd
from pathlib import Path
import discord
from discord import app_commands
from .read_embree_csv import read_embree_csv_raw

TW_EMBREE_CSV_PATH = Path(__file__).parent / "ChhoeTaigi_EmbreeTaiengSutian.csv"
TW_EMBREE_CSV = read_embree_csv_raw(TW_EMBREE_CSV_PATH)

def get_random_row(df: pd.DataFrame) -> pd.Series:
    return df.sample().iloc[0]

def register_commands(
    tree: discord.app_commands.CommandTree,
    this_guild: discord.Object,
    client: discord.Client,
):
    taigi_group = app_commands.Group(
        name="taigi", description="Taiwanese commands"
    )

    @taigi_group.command(
        name="random",
        description="Get a random Taiwanese word",
    )
    async def taigi_rand(
        interaction: discord.Interaction,
    ):
        random_row = get_random_row(TW_EMBREE_CSV)
        # testing: just print the random row
        await interaction.response.send_message(
            f"Random word from Taiwanese word list:", content=str(random_row)
        )
        # embed = _create_word_embed(
        #     random_row["PojUnicode"],
        #     random_row["Abbreviation"],
        #     random_row["NounClassifier"],
        #     random_row["HoaBun"],
        #     random_row["EngBun"],
        # )
        # await interaction.response.send_message(
        #     f"Random word from Taiwanese word list:", embed=embed
        # )
