import datetime
import json
import os
import sys
import discord
from dotenv import load_dotenv

from modules.db import get_cursor

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


async def log_event(
    message: discord.Message | discord.Interaction,
    data: dict = {},
    content: str = None,
    color: discord.Color = None,
    log_to_channel=True,
):
    metadata = data.get("metadata")
    row = {
        "message_id": message.id if message.id else None,
        "event": data.get("event"),
        "created_at": str(message.created_at),
        "content": content if content else (message.content if hasattr(message, 'content') else None),
        "author_id": data.get("author_id", message.author.id if hasattr(message, 'author') else None),
        "mentioned_id": data.get("mentioned_id"),
        "channel_id": message.channel.id if message.channel else None,
        "guild_id": message.guild.id if message.guild else None,
        "generated_id": data.get("generated_id"),
        "metadata": json.dumps(metadata) if metadata is not None else None,
    }
    with get_cursor() as cur:
        cur.execute(
            """
            INSERT INTO event_logs
                (message_id, event, created_at, content, author_id, mentioned_id,
                 channel_id, guild_id, generated_id, metadata)
            VALUES
                (%(message_id)s, %(event)s, %(created_at)s, %(content)s, %(author_id)s, %(mentioned_id)s,
                 %(channel_id)s, %(guild_id)s, %(generated_id)s, %(metadata)s)
            """,
            row,
        )
    if log_to_channel:
        await logging.log_to_channel(data, color)
    print(row)


async def log_message_event(message: discord.Message, events: list[str]):
    rows = [
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
    with get_cursor() as cur:
        for row in rows:
            cur.execute(
                """
                INSERT INTO message_logs (message_id, author_id, event, created_at, channel_id, guild_id)
                VALUES (%(message_id)s, %(author_id)s, %(event)s, %(created_at)s, %(channel_id)s, %(guild_id)s)
                """,
                row,
            )
    print(rows)


async def fetch_event_log(guild_id: int, generated_id: str, event: str):
    with get_cursor() as cur:
        cur.execute(
            "SELECT * FROM event_logs WHERE guild_id = %s AND generated_id = %s AND event = %s",
            (guild_id, generated_id, event),
        )
        return cur.fetchall()
