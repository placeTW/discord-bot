# note: this might need to become async
def modify_json_and_create_pull_request(
    lang: str,  # en, lt, et, etc
    entry_id: int,  # entry INDEX (i.e., from 0 to 15)
    entry_name: str,  # entry id
    field: str,  # title, desc, etc
    proposed_text: str,
):
    print("Fetching the relevant json file from url...")
    print("Modifying the json to reflect the changes...")
    print("Creating a pull request...")
    print("Done!")
    pass
