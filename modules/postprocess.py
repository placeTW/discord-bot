"""
This file stores functions that are used to postprocess
output before they are sent to the user. For example,
turning a list of links into a markdown string.
"""


def postprocess_fetch_field(to_print) -> str:
    """Postprocess one field (not an entire entry.)

    Args:
        to_print (str|list): A string or list.

    Returns:
        str: string to send to user.
    """
    if type(to_print) is list:
        to_print = [f"* {p}" for p in to_print]
        to_print = "\n".join(to_print)
    return to_print


def postprocess_fetch_item(entry: dict) -> str:
    """Postprocess an entire entry into a string.

    Args:
        entry (dict): the entry.

    Returns:
        str: string to send to user.
    """
    title = f"# {entry['title']}"
    blurb = f"{entry['blurb']}"
    desc = f"## Description\n{entry['desc']}"
    links = f"## External Links\n{postprocess_fetch_field(entry['links'])}"
    return "\n".join([title, blurb, desc, links])
