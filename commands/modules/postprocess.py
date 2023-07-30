def postprocess_fetch_field(to_print):
    if type(to_print) is list:
        to_print = [f"* {p}" for p in to_print]
        to_print = "\n".join(to_print)
    return to_print


def postprocess_fetch_item(entry: dict):
    title = f"# {entry['title']}"
    blurb = f"{entry['blurb']}"
    desc = f"## Description\n{entry['desc']}"
    links = f"## External Links\n{postprocess_fetch_field(entry['links'])}"
    return "\n".join([title, blurb, desc, links])
