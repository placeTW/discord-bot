import discord

from ..modules.supabase import supabaseClient

def get_pat_stats(pat_type: str):
    data, c = supabaseClient.table(f'total_{pat_type}_counts').select("*").limit(10).execute()
    if c == 0:
        return None

    top_patted_users = data[1]
    embed = discord.Embed(title=f"Top 10 {pat_type}", color=discord.Color.blue())
    embed.description = '\n'.join([f"{i+1}. <@{user_data['id']}>: {user_data['count']}" for i, user_data in enumerate(top_patted_users)])
    return embed