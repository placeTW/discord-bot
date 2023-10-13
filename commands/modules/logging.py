import datetime
import os
import sys
import discord
from dotenv import load_dotenv
load_dotenv()

FILENAME = f"{str(datetime.datetime.now()).split('.')[0].replace(':', '-')}.log"
path = f"{sys.path[0]}/logs/{FILENAME}"


class Logging:
    def __init__(self):
        self.log_channel = None

    def set_log_channel(self, channel):
        self.log_channel = channel

    async def log(self, event, log_data: dict):
        print(event)
        try:
            file_object = open(path, 'a')
            file_object.write(f"{datetime.datetime.now()}: {event}\n")
            file_object.close()
        except:
            print('!!! failed to write log entry to file')
        if not self.log_channel is None:
            embed = discord.Embed()
            for param in log_data.items():
                embed.add_field(name=param[0], value=param[1], inline=False)
            await self.log_channel.send(embed=embed)


logging = Logging()


def init(client: discord.Client):
    log_channel = client.get_channel(int(os.getenv('LOG_CHANNEL')))
    logging.set_log_channel(log_channel)


async def log(message, data: dict = {}):
    await logging.log(message, data)
