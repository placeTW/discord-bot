"""Validates the object detection model with validation data.

Reference:
- https://github.com/alankbi/detecto
- https://detecto.readthedocs.io/en/latest/usage/quickstart.html
- https://detecto.readthedocs.io/en/latest/usage/further-usage.html
"""

from detecto.core import Dataset, Model
from matplotlib import pyplot as plt


def main() -> None:
    # Load images and label data from the folder
    dataset = Dataset("training_data/")
    val_dataset = Dataset("validation_data/")

    # Load the model from the file
    classes: list[str] = ["boba"]
    model = Model.load("models/boba.pth", classes)

    # Calculate the losses
    losses = model.fit(
        dataset,
        val_dataset,
        epochs=10,
        learning_rate=0.01,
        gamma=0.2,
        lr_step_size=5,
        verbose=True,
    )

    plt.plot(losses)
    plt.show()


if __name__ == "__main__":
    main()
