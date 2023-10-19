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

    async def log_to_channel(self, log_text, log_data: dict):
        print(log_text)
        try:
            file_object = open(self.log_file_path, 'a')
            file_object.write(f"{datetime.datetime.now()}: {log_text}\n")
            file_object.close()
        except:
            print('!!! failed to write log entry to file')
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


async def log_to_channel(log_text: str, message: discord.Message, data: dict = {}):
    await logging.log_to_channel(log_text, data)


async def log_message_event(message: discord.Message, events: list[str]):
    data = supabase.table('message_logs').insert([
        {
            "message_id": message.id,
            "author_id": message.author.id,
            "event": event,
            "created_at": str(message.created_at),
            "channel_id": message.channel.id,
            "guild_id": message.guild.id if not message.guild is None else None,
        }
        for event in events]).execute()
    print(data)
