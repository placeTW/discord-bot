from supabase import create_client, Client
import datetime
import os
import sys
import discord
from dotenv import load_dotenv
load_dotenv()


url: str = os.getenv("SUPABASE_URL")
private_key: str = os.getenv("SUPABASE_SECRET_KEY")
supabase: Client = create_client(url, private_key)


class Logging:
    def __init__(self):
        self.log_channel = None
        self.log_file_path = None

    def set_log_params(self, channel, log_file):
        self.log_channel = channel
        self.log_file_path = log_file

    async def log_to_channel(self, log_data: dict):
        if not self.log_channel is None:
            embed = discord.Embed()
            for param in log_data.items():
                embed.add_field(name=param[0], value=param[1], inline=False)
            await self.log_channel.send(embed=embed)


logging = Logging()


def init(client: discord.Client, deployment_date: datetime):
    log_channel = client.get_channel(int(os.getenv('LOG_CHANNEL')))
    filename = f"{str(deployment_date).split('.')[0].replace(':', '-')}.log"
    path = f"{sys.path[0]}/logs/{filename}"
    logging.set_log_params(log_channel, path)

"""

"""
async def log_to_channel(message: discord.Message, data: dict = {}, content: str = None):
    supabase.table('event_logs').insert(
    {
        "event": data['event'] if 'event' in data else None,
        "generated_id": data['generated_id'] if 'generated_id' in data else None,
        "created_at": str(message.created_at),
        "author_id": data['author_id'] if 'author_id' in data else message.author.id,
        "channel_id": message.channel.id,
        "guild_id": message.guild.id if message.guild else None,
        "content": content if content else message.content,
    }).execute()
    await logging.log_to_channel(data)


async def log_message_event(message: discord.Message, events: list[str]):
    data = supabase.table('message_logs').insert([
        {
            "message_id": message.id,
            "author_id": message.author.id,
            "event": event,
            "created_at": str(message.created_at),
            "channel_id": message.channel.id,
            "guild_id": message.guild.id if message.guild else None,
        }
        for event in events]).execute()
    print(data)
