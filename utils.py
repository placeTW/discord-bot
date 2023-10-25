import json
import hjson


def read_json_file(filename: str):
    """Reads a json file and returns the contents as a dictionary.

    Args:
        filename (str): The filename of the json file to read.

    Returns:
        dict: The contents of the json file.
    """
    with open(filename, "r") as f:
        return json.load(f)


def read_hjson_file(filename: str):
    """Reads a hjson file and returns the contents as a dictionary.

    Args:
        filename (str): The filename of the hjson file to read.

    Returns:
        dict: The contents of the hjson file.
    """
    with open(filename, "r") as f:
        return hjson.load(f)
