from modules.supabase import supabaseClient

TABLE = "tocfl"

def get_random_tocfl_choices_from_db(num_choices=5):
    command_name = "get_random_unique_pinyin"
    data, c = supabaseClient.rpc(
        command_name,
        {"number_of_entries": num_choices},
    ).execute()
    if c == 0:
        return None
    return data[1]

if __name__ == "__main__":
    choices = get_random_tocfl_choices_from_db()
    print(choices)