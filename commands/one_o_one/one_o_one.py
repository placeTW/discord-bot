from collections import deque
from enum import Enum
from typing import Final
import random
import time

import discord


class BuildingTypes(Enum):
    """Building types and their weights (the higher the weight, the easier it
    is to be chosen).
    """

    NORMAL_ROOF = 10
    NO_ROOF = 3
    TROLL_ROOF = 2
    TROLL_BODY = 1


class OneOOne:
    COOL_DOWN_DURATION: Final[int] = 30  # in seconds
    MAX_TIMESTAMPS: Final[int] = 3  # max number of timestamps to save per user

    EMOJI_101_FLOOR: Final[str] = "<:101_Floor:1132608196515725332>"
    EMOJI_101_TOP: Final[str] = "<:101_Top:1132608896222113951>"
    EMOJI_BUBBLE_MILK_TEA: Final[str] = "<:bubblemilktea:1132632348651966596>"
    EMOJI_ROC_TROLL: Final[str] = "<:roc_troll:1133368648967405610>"
    EMOJI_TSMC_LOGO: Final[str] = "<:tsmclogo:1132883401951694938>"
    EMOJI_TW_AMOGUS: Final[str] = "<:tw_amogus:1133361653908516885>"

    TROLL_ROOFS: Final[list[str]] = [EMOJI_101_TOP, EMOJI_BUBBLE_MILK_TEA]
    TROLL_BODIES: Final[list[str]] = [
        EMOJI_ROC_TROLL,
        EMOJI_TSMC_LOGO,
        EMOJI_TW_AMOGUS,
    ]

    MIN_NUM_FLOORS: Final[int] = 1
    MAX_NUM_FLOORS: Final[int] = 50  # not 101?

    def __init__(self) -> None:
        # Store the deque of call timestamps for each user
        self._user_to_timestamps: dict[int, deque] = {}

    def get_message(self, user: int) -> str:
        if self._is_rate_limited(user):
            user_mention = f"<@{user}>"
            messages: list[str] = [
                "Congrats! You've unlocked the 'Wait and Retry Later' achievement!",
                f"{user_mention} is on :fire:! No worries, cooldown is here to cool you down",
                "Whoa there, please slow down. My slow server brain couldn't catch up",
                f"Cooldown mode activated. Great job {user_mention}.",
                "If you keep doing this, I'm gonna shove 101 down your throat",
                "Did you just type the command again to see if cooldown has been deactivated? Let me tell you: NO",
                "What have I told you. Stop it.",
                "Give it up. It's just random string. I'm not an AI (or I'm pretending not to be?)",
                f"Social credit score -999 for {user_mention}",
            ]
            return random.choice(messages)
        else:
            self._update_rate_limit_timestamp(user)
            return self._build_101()

    def _build_101(self) -> str:
        building_type = self._get_random_building_type()

        messages: list[str] = []
        messages.extend(self._build_101_roofs(building_type))
        messages.extend(self._build_101_bodies(building_type))
        return "\n".join(messages)

    def _get_random_building_type(self) -> BuildingTypes:
        building_types = [option for option in BuildingTypes]
        weights = [option.value for option in BuildingTypes]
        return random.choices(building_types, weights=weights)[0]

    def _build_101_roofs(self, building_type: BuildingTypes) -> list[str]:
        if building_type == BuildingTypes.NORMAL_ROOF:
            return [self.EMOJI_101_TOP]
        elif building_type == BuildingTypes.TROLL_ROOF:
            return [random.choice(self.TROLL_ROOFS)]
        elif building_type == BuildingTypes.TROLL_BODY:
            return [self.EMOJI_101_TOP]
        else:
            return []

    def _build_101_bodies(self, building_type: BuildingTypes) -> list[str]:
        num_floors = random.randint(self.MIN_NUM_FLOORS, self.MAX_NUM_FLOORS)
        bodies: list[str] = [self.EMOJI_101_FLOOR for _ in range(num_floors)]

        if building_type == BuildingTypes.TROLL_BODY:
            troll_body = random.choice(self.TROLL_BODIES)
            random_index = random.randint(0, num_floors - 1)
            bodies[random_index] = troll_body

        return bodies

    def _is_rate_limited(self, user: int) -> bool:
        timestamps = self._user_to_timestamps.get(user, None)
        if timestamps is None:
            return False

        current_time = time.time()

        # Remove older timestamps from the deque that are outside the cool down
        # window
        while timestamps and current_time - timestamps[0] > self.COOL_DOWN_DURATION:
            timestamps.popleft()

        # Don't rate limit until user has many timestamps
        if len(timestamps) < self.MAX_TIMESTAMPS:
            return False

        # Calculate the average time user calls the command
        average_call_time = (current_time - timestamps[0]) / len(timestamps)

        return average_call_time <= self.COOL_DOWN_DURATION

    def _update_rate_limit_timestamp(self, user: int) -> None:
        if user not in self._user_to_timestamps:
            self._user_to_timestamps[user] = deque()

        current_time = time.time()
        self._user_to_timestamps[user].append(current_time)


def register_commands(tree, guilds: list[discord.Object]) -> None:
    one_o_one = OneOOne()

    @tree.command(
        name="101",
        description="Wanna build your own Taipei 101?",
        guilds=guilds,
    )
    async def command(interaction: discord.Interaction):
        message = one_o_one.get_message(interaction.user.id)
        await interaction.response.send_message(message)
