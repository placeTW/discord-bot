import discord
import datetime
import logging
import sys


TW_SERVER_CONFESSIONS_CHANNEL_ID = 1161839912509775902
BALTICS_SERVER_CONFESSIONS_CHANNEL_ID = 1161419086987800737
TW_SERVER_CONFESSIONS_CHANNEL_OBJ = discord.Object(
    id=TW_SERVER_CONFESSIONS_CHANNEL_ID
)
BALTICS_SERVER_CONFESSIONS_CHANNEL_OBJ = discord.Object(
    id=BALTICS_SERVER_CONFESSIONS_CHANNEL_ID
)


filename = f"{str(datetime.datetime.now()).split('.')[0].replace(':', '-')}.log"
path = f"{sys.path[0]}/logs/{filename}"
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S', level=logging.INFO, filename=path, filemode='a')
logging.getLogger().addHandler(logging.StreamHandler())

def register_commands(
    tree: discord.app_commands.CommandTree,
    client: discord.Client,
    guilds: list,
):
    @tree.command(
        name="confess",
        description="Make an anonymous confession",
        guilds=[  # TW and Baltics server
            discord.Object(id=guilds[0]),
            discord.Object(id=guilds[1]),
        ],
    )
    async def confess(interaction: discord.Interaction, confession: str):
        """Write an anonymous confession.

        Args:
            interaction (discord.Interaction): required by discord.py
            confession (str): The confession to make.
        """
        server = (
            "TW" if (interaction.guild_id == int(guilds[0])) else "BALTICS"
        )
        confession_channel_id = (
            TW_SERVER_CONFESSIONS_CHANNEL_ID
            if server == "TW"
            else BALTICS_SERVER_CONFESSIONS_CHANNEL_ID
        )
        confession_channel = client.get_channel(confession_channel_id)
        embed = discord.Embed()
        embed.add_field(name="Confession", value=confession, inline=False)
        logging.info(f"({server}) {interaction.user.name}: {confession}")
        await confession_channel.send(embed=embed)
        await interaction.response.send_message(
            f"Your confession has been sent to <#{confession_channel_id}>.",
            ephemeral=True,
        )
