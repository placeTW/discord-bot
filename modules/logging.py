from supabase import create_client, Client
import datetime
import os
import sys
import discord
from modules.supabase import supabaseClient

from dotenv import load_dotenv
from .supabase import supabaseClient

load_dotenv()


class Logging:
    def __init__(self):
        self.log_channel: discord.TextChannel = None
        self.log_file_path = None

    def set_log_params(self, channel, log_file):
        self.log_channel = channel
        self.log_file_path = log_file

    async def log_to_channel(self, log_data: dict, color: discord.Color = None):
        if not self.log_channel is None:
            embed = discord.Embed(color=color if color else discord.Color.default())
            for param in log_data.items():
                embed.add_field(name=param[0], value=param[1], inline=False)
            await self.log_channel.send(embed=embed)


logging = Logging()


def init(client: discord.Client, deployment_date: datetime):
    log_channel = client.get_channel(int(os.getenv("LOG_CHANNEL")))
    filename = f"{str(deployment_date).split('.')[0].replace(':', '-')}.log"
    path = f"{sys.path[0]}/logs/{filename}"
    logging.set_log_params(log_channel, path)


"""

"""


async def log_event(
    message: discord.Message | discord.Interaction,
    data: dict = {},
    content: str = None,
    color: discord.Color = None,
    log_to_channel=True,
):
    supabaseClient.table("event_logs").insert(
        {
            "message_id": message.id if message.id else None,
            "event": data["event"] if "event" in data else None,
            "created_at": str(message.created_at),
            "content": content if content else message.content if hasattr(message, 'content') else None,
            "author_id": data["author_id"] if "author_id" in data else message.author.id,
            "mentioned_id": data["mentioned_id"] if "mentioned_id" in data else None,
            "channel_id": message.channel.id if message.channel else None,
            "guild_id": message.guild.id if message.guild else None,
            "generated_id": data["generated_id"] if "generated_id" in data else None,
            "metadata": data["metadata"] if "metadata" in data else None,
        }
    ).execute()
    if log_to_channel:
        await logging.log_to_channel(data, color)


async def log_message_event(message: discord.Message, events: list[str]):
    data = (
        supabaseClient.table("message_logs")
        .insert(
            [
                {
                    "message_id": message.id,
                    "author_id": message.author.id,
                    "event": event,
                    "created_at": str(message.created_at),
                    "channel_id": message.channel.id if message.channel else None,
                    "guild_id": message.guild.id if message.guild else None,
                }
                for event in events
            ]
        )
        .execute()
    )
    print(data)


async def fetch_event_log(guild_id: int, generated_id: str, event: str):
    return (
        supabaseClient.table("event_logs")
        .select("*")
        .eq("guild_id", guild_id)
        .eq("generated_id", generated_id)
        .eq("event", event)
        .execute()
        .data
    )
