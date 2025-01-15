from modules.supabase import supabaseClient


def fetch_configs(is_prod: bool):
    supabase_data = supabaseClient.table("server_config").select("*").eq('prod_config', is_prod).execute().data
    transformed_dict = {
        item['guild_id']: {key: value for key, value in item.items() if key != 'guild_id'} for item in supabase_data
    }
    return transformed_dict


def fetch_guild_config(guild_id: int, is_prod: bool):
    response = supabaseClient.table("server_config").select("*").eq("guild_id", guild_id).eq(
        "prod_config", is_prod
    ).execute()
    # if there is no data, return an empty dict
    if len(response.data) == 0:
        return {}
    return response.data[0]

def create_new_config(guild_id: int, server_name: str, is_prod: bool):
    response = supabaseClient.table("server_config").insert(
        {
            "guild_id": guild_id,
            "server_name": server_name,
            "prod_config": is_prod,
        }
    ).execute()
    return response.data


def set_config(guild_id: int, key: str, value: str, is_prod: bool) -> list:
    response = supabaseClient.table("server_config").update({key: value}).eq("guild_id", guild_id).eq(
        "prod_config", is_prod
    ).execute()
    return response.data

def remove_config(guild_id: int, is_prod: bool) -> list:
    response = supabaseClient.table("server_config").delete().eq("guild_id", guild_id).eq(
        "prod_config", is_prod
    ).execute()
    return response.data

