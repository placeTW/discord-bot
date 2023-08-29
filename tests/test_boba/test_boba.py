from pathlib import Path

from PIL import Image

from commands.boba.boba import make_avatar_circular


def test_make_avatar_circular() -> None:
    script_dir = Path(__file__).parent
    pfp = Image.open(script_dir / "png_test.png")
    circular_pfp = make_avatar_circular(pfp)

    expected_circular_pfp = Image.open(script_dir / "round_png_test.png")
    assert is_images_equal(circular_pfp, expected_circular_pfp)


def is_images_equal(image1: Image.Image, image2: Image.Image) -> bool:
    if image1.size != image2.size:
        return False

    pixel_data1 = image1.convert("RGBA").tobytes()
    pixel_data2 = image2.convert("RGBA").tobytes()

    return pixel_data1 == pixel_data2
