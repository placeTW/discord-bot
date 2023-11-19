import datetime
import discord
from re import compile, IGNORECASE, UNICODE
from ..react_baltics.react_baltics import mock_bernoulli

KEYWORDS = ("HSINCHU", "新竹")

HSINCHU_REGEX = compile(
    rf"(?:{'|'.join(KEYWORDS)})", flags=IGNORECASE | UNICODE
)


class HsinchuWind:
    COOLDOWN_TIME_IN_MINUTES = datetime.timedelta(minutes=5)
    HSINCHU_LINK = "https://www.youtube.com/watch?v=EtGDGCxq6m8"

    def __init__(self) -> None:
        self.latest_sent_time = None

    def set_latest_sent_time_to_now(self):
        self.latest_sent_time = datetime.datetime.now()

    def is_cooldown_over(self):
        return True  # this is for you, ht
        if self.latest_sent_time is None:
            return True
        now_time = datetime.datetime.now()
        elapsed = now_time - self.latest_sent_time
        return elapsed > self.COOLDOWN_TIME_IN_MINUTES

    def get_response_or_ignore(self):
        if self.is_cooldown_over():
            self.set_latest_sent_time_to_now()
            return self.HSINCHU_LINK
        else:
            # print("still on cooldown!")
            return None


hsinchu_wind = HsinchuWind()


def is_hsinchu_message(message: discord.Message):
    return HSINCHU_REGEX.search(message.content)


async def send_hsinchu_msg(message: discord.Message):
    text = hsinchu_wind.get_response_or_ignore()
    if text is not None and mock_bernoulli(0.15):
        await message.reply(text)
