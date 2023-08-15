import random
import traceback
from io import BytesIO
from pathlib import Path
from typing import Final

import discord
from detecto.core import Model
from discord import app_commands
from PIL import Image, ImageDraw

from commands.modules.probability import mock_bernoulli
from pathlib import Path

BOBA_DIR = Path(__file__).parent  # this file's dir


def register_commands(tree, this_guild: discord.Object):
    # Load the model from the file
    classes: list[str] = ["boba"]
    model_path = BOBA_DIR / "models/boba.pth"
    if not model_path.is_file():
        print("Model not found, this command will not be registered.")
        return
    model = Model.load(str(model_path), classes)

    image_files = (
        load_images_under_directory(BOBA_DIR / "random_images")
        + load_images_under_directory(BOBA_DIR / "training_images")
        + load_images_under_directory(BOBA_DIR / "validation_data")
    )
    if not image_files:
        raise RuntimeError(f"Should have at least one image")

    @tree.command(
        name="boba",
        description="Give boba someone to drink",
        guild=this_guild,
    )
    @app_commands.rename(user="member")
    async def boba(interaction: discord.Interaction, user: discord.Member):
        if user.avatar is None:
            return await interaction.response.send_message("No avatar?")
        if interaction.channel is None:
            return await interaction.response.send_message("No channel?")

        # Tell Discord that this command may run for some time, wait for me
        await interaction.response.defer()

        try:
            # Fetch the user's profile picture
            avatar_url = user.avatar.with_size(256)
            response = await avatar_url.read()
            original_pfp = Image.open(BytesIO(response))
            rgba_pfp = convert_image_to_rgba(original_pfp)

            # Make a circular mask
            round_pfp = make_avatar_circular(rgba_pfp)

            # Choose a random image file
            random_image_file = random.choice(image_files)

            # Load the random image using Pillow
            background_image = Image.open(random_image_file)
            rgba_background = convert_image_to_rgb(background_image)

            # Make predictions
            predictions = model.predict(rgba_background)

            # Add pfp on predicted bounding boxes
            composite_image = add_pfp_on_prediction_boxes(
                rgba_background, round_pfp, predictions
            )

            # Save the composite image
            composite_path = str(BOBA_DIR / "boba_with_pfp.png")
            composite_image.save(composite_path)

            # Send the message
            await interaction.followup.send(
                f"<@{user.id}>'s boba tea is ready"
            )

            # Send the composite image as a response
            await interaction.followup.send(file=discord.File(composite_path))
        except Exception as ex:
            tb = traceback.format_exc()
            await interaction.followup.send(
                f"Your command went wrong who wrote this shit: {ex}\n"
                f"```\n{tb}\n```"
            )


def load_images_under_directory(directory: Path) -> list[Path]:
    # List of image extensions to consider
    image_extensions: Final[list[str]] = [".jpg", ".jpeg", ".png", ".gif"]

    # Get a list of image files in the directory with the specified extensions
    return [
        file
        for file in directory.glob("*")
        if file.suffix.lower() in image_extensions
    ]


def add_pfp_on_prediction_boxes(
    background: Image.Image, pfp: Image.Image, predictions
) -> Image.Image:
    max_num_pfp: Final[int] = 10
    min_score: Final[float] = 0.3
    cancel_chance: Final[float] = 0.5
    scale_factor: Final[float] = 1.5

    label, boxes, scores = predictions
    num_boba = 0
    for box, score in zip(boxes, scores):
        # Limit the maximum number of boxes to paste pfp
        if num_boba >= max_num_pfp:
            break

        # Discard the bounding box if the score is too low
        if score < min_score:
            continue

        # Don't cover all boba
        if mock_bernoulli(cancel_chance):
            continue

        x1, y1, x2, y2 = box
        # Get the floats from tensors
        x1 = int(x1.item())
        y1 = int(y1.item())
        x2 = int(x2.item())
        y2 = int(y2.item())
        # Scale it
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2
        width = int((x2 - x1) * scale_factor)
        height = int((y2 - y1) * scale_factor)
        paste_x = center_x - width // 2
        paste_y = center_y - height // 2

        # Check if the size is valid
        if width <= 0 or height <= 0:
            continue

        # Check if the pasting location is valid
        if (
            paste_x < 0
            or paste_y < 0
            or paste_x + width > background.width
            or paste_y + height > background.height
        ):
            continue

        # Randomly select a rotation angle
        rotation_angle = random.randint(0, 60) - 30

        # Rotate the image
        rotated_pfp = pfp.rotate(rotation_angle, expand=True)

        # Resize the picture
        resized_pfp = rotated_pfp.resize((width, height))

        # Paste the picture on the background image
        background.paste(resized_pfp, (paste_x, paste_y), resized_pfp)

        num_boba += 1

    return background


def convert_image_to_rgb(image: Image.Image) -> Image.Image:
    # Create a new RGBA image with the same size as the JPEG image
    rgb_image = Image.new("RGB", image.size)

    # Paste the JPEG image onto the RGB image
    rgb_image.paste(image, (0, 0))

    return rgb_image


def convert_image_to_rgba(image: Image.Image) -> Image.Image:
    # Create a new RGBA image with the same size as the JPEG image
    rgba_image = Image.new("RGBA", image.size)

    # Paste the JPEG image onto the RGBA image
    rgba_image.paste(image, (0, 0))

    return rgba_image


def make_avatar_circular(image: Image.Image) -> Image.Image:
    # Create a mask with the same size as the image, initially filled with black (0)
    mask = Image.new("L", image.size, 0)

    # Create a drawing object for the mask
    draw = ImageDraw.Draw(mask)

    # Draw a white ellipse on the mask, covering the entire image area
    draw.ellipse((0, 0) + image.size, fill=255)

    # Create a new mask image with the same size as the image
    mask_image = Image.new("L", image.size, 0)

    # Paste the circular mask onto the new mask image, using the alpha channel of the original image
    mask_image.paste(mask, (0, 0), image.getchannel("A"))

    # Create a new RGBA image with the same size as the original image
    output = Image.new("RGBA", image.size)

    # Paste the original image onto the output image using the circular mask
    output.paste(image, (0, 0), mask_image)

    return output
