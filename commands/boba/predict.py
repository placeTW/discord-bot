"""Validates the object detection model with validation data.

Reference:
- https://github.com/alankbi/detecto
- https://detecto.readthedocs.io/en/latest/usage/quickstart.html
- https://detecto.readthedocs.io/en/latest/usage/further-usage.html
"""

from detecto.core import Dataset, Model
from detecto.visualize import plot_prediction_grid


def main() -> None:
    # Load images and label data from the folder
    dataset = Dataset("training_data/")

    # Load the model from the file
    classes: list[str] = ["boba"]
    model = Model.load("models/boba.pth", classes)

    # Predict by using a single image
    image = get_ith_image(dataset, 0)
    predictions = model.predict(image)
    print(predictions)
    plot_prediction_grid(model, [image], dim=(1, 1), figsize=(8, 8))


def get_ith_image(dataset: Dataset, index: int):
    image, _ = dataset[index]
    return image


if __name__ == "__main__":
    main()
