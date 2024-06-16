from modules.supabase import supabaseClient

def fetch_config(is_prod: bool):
  supabase_data = supabaseClient.table("server_config").select("*").eq('prod_config', is_prod).execute().data
  transformed_dict = {item['guild_id']: {key: value for key, value in item.items() if key != 'guild_id'} for item in supabase_data}
  return transformed_dict

def set_config(guild_id: int, key: str, value: str, is_prod: bool):
    supabaseClient.table("server_config").update({key: value}).eq("guild_id", guild_id).eq("prod_config", is_prod).execute()
