def postprocess_fetch_item(to_print):
    if type(to_print) is list:
        to_print = [f"* {p}" for p in to_print]
        to_print = "\n".join(to_print)
    return to_print
