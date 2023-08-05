import random
import time
from unittest.mock import MagicMock, patch

from commands.one_o_one.one_o_one import BuildingTypes, OneOOne


@patch.object(random, "randint")
@patch.object(OneOOne, "_get_random_building_type")
def test_normal_roof(
    mock_get_random_building_type: MagicMock, mock_randint: MagicMock
) -> None:
    # Set the return values for the mocked functions
    mock_get_random_building_type.return_value = BuildingTypes.NORMAL_ROOF
    mock_randint.return_value = 3

    one_o_one = OneOOne()
    expected_message = "\n".join(
        [
            OneOOne.EMOJI_101_TOP,
            OneOOne.EMOJI_101_FLOOR,
            OneOOne.EMOJI_101_FLOOR,
            OneOOne.EMOJI_101_FLOOR,
        ]
    )
    assert one_o_one.get_message(123) == expected_message


@patch.object(random, "randint")
@patch.object(OneOOne, "_get_random_building_type")
def test_no_roof(
    mock_get_random_building_type: MagicMock, mock_randint: MagicMock
) -> None:
    # Set the return values for the mocked functions
    mock_get_random_building_type.return_value = BuildingTypes.NO_ROOF
    mock_randint.return_value = 3

    one_o_one = OneOOne()
    expected_message = "\n".join(
        [
            OneOOne.EMOJI_101_FLOOR,
            OneOOne.EMOJI_101_FLOOR,
            OneOOne.EMOJI_101_FLOOR,
        ]
    )
    assert one_o_one.get_message(123) == expected_message


@patch.object(random, "randint")
@patch.object(OneOOne, "_build_101_roofs")
@patch.object(OneOOne, "_get_random_building_type")
def test_troll_roof(
    mock_get_random_building_type: MagicMock,
    _build_101_roofs: MagicMock,
    mock_randint: MagicMock,
) -> None:
    # Set the return values for the mocked functions
    mock_get_random_building_type.return_value = BuildingTypes.TROLL_ROOF
    _build_101_roofs.return_value = [OneOOne.EMOJI_ROC_TROLL]
    mock_randint.return_value = 3

    one_o_one = OneOOne()
    expected_message = "\n".join(
        [
            OneOOne.EMOJI_ROC_TROLL,
            OneOOne.EMOJI_101_FLOOR,
            OneOOne.EMOJI_101_FLOOR,
            OneOOne.EMOJI_101_FLOOR,
        ]
    )
    assert one_o_one.get_message(123) == expected_message


@patch.object(random, "choice")
@patch.object(random, "randint")
@patch.object(OneOOne, "_get_random_building_type")
def test_troll_body(
    mock_get_random_building_type: MagicMock,
    mock_randint: MagicMock,
    mock_choice: MagicMock,
) -> None:
    def randint_side_effect(a, b) -> int:
        if a == OneOOne.MIN_NUM_FLOORS:  # for number of floors
            return 3
        else:  # for random troll body index
            return 1

    # Set the return values for the mocked functions
    mock_get_random_building_type.return_value = BuildingTypes.TROLL_BODY
    mock_choice.return_value = OneOOne.EMOJI_TW_AMOGUS

    # Set the side effect for the mocked functions
    mock_randint.side_effect = randint_side_effect

    one_o_one = OneOOne()
    expected_message = "\n".join(
        [
            OneOOne.EMOJI_101_TOP,
            OneOOne.EMOJI_101_FLOOR,
            OneOOne.EMOJI_TW_AMOGUS,
            OneOOne.EMOJI_101_FLOOR,
        ]
    )
    assert one_o_one.get_message(123) == expected_message


@patch.object(time, "time")
@patch.object(OneOOne, "_get_random_building_type")
def test_rate_limiting(
    mock_get_random_building_type: MagicMock,
    mock_time: MagicMock,
) -> None:
    num_time_calls = 0

    def time_side_effect() -> int:
        # Returns 1, 2, 3, ...
        nonlocal num_time_calls
        num_time_calls += 1
        return num_time_calls

    # Set the return values for the mocked functions
    mock_get_random_building_type.return_value = BuildingTypes.NORMAL_ROOF

    # Set the side effect for the mocked functions
    mock_time.side_effect = time_side_effect

    one_o_one = OneOOne()
    for _ in range(OneOOne.MAX_TIMESTAMPS):
        assert OneOOne.EMOJI_101_FLOOR in one_o_one.get_message(123)

    # Will get rate limited because it simulates user sending message per
    # second by the time side effect
    assert OneOOne.EMOJI_101_FLOOR not in one_o_one.get_message(123)
