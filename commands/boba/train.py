"""Trains object detection model with training data.

Reference:
- https://github.com/alankbi/detecto
- https://detecto.readthedocs.io/en/latest/usage/quickstart.html
- https://detecto.readthedocs.io/en/latest/usage/further-usage.html
"""

from detecto.core import Dataset, Model
from detecto.utils import normalize_transform
from matplotlib import pyplot as plt
from torchvision import transforms


def main() -> None:
    # Apply custom transformations
    custom_transforms = transforms.Compose(
        [
            transforms.ToPILImage(),
            # Note: all images with a size smaller than 800 will be scaled up in size
            transforms.Resize(800),
            transforms.ColorJitter(saturation=0.3),
            transforms.ToTensor(),  # required
            normalize_transform(),  # required
        ]
    )

    # Load images and label data from the folder
    dataset = Dataset("training_data/", transform=custom_transforms)

    # Train to predict some labels (only boba for now)
    classes: list[str] = ["boba"]
    model = Model(classes)
    model.fit(
        dataset,
        epochs=3,
        learning_rate=0.001,
        verbose=True,
    )

    # Save the trained model
    model.save("models/boba.pth")


if __name__ == "__main__":
    main()
