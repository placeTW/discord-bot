import datetime
from ..modules.supabase import supabaseClient

TABLE = "bubble_tea_entries"


def add_bbt_entry(
    created_at: datetime,
    user_id: int,
    guild_id: int,
    location: str,
    description: str,
):
    response = (
        supabaseClient.table(TABLE)
        .insert(
            {
                "created_at": str(created_at),
                "user_id": user_id,
                "guild_id": guild_id,
                "location": location,
                "description": description,
            }
        )
        .execute()
    )
    print(response)
    return response.data[0]["id"]


def remove_bbt_entry(id: int, user_id: int):
    response = (
        supabaseClient.table(TABLE)
        .delete()
        .match(
            {
                "id": id,
                "user_id": user_id,
            }
        )
        .execute()
    )
    print(response)


def get_bbt_entries(user_id: int, year: int = None):
    data, c = (
        supabaseClient.table(TABLE)
        .select("*")
        .lte(
            "created_at",
            str(
                datetime.datetime.now() + datetime.timedelta(days=1)
                if year is None
                else datetime.datetime(year, 12, 31)
            ),
        )
        .gte(
            "created_at",
            str(
                datetime.datetime.now() - datetime.timedelta(days=365)
                if year is None
                else datetime.datetime(year, 1, 1)
            ),
        )
        .match(
            {
                "user_id": user_id,
            }
        )
        .order("created_at", desc=True)
        .execute()
    )
    if c == 0:
        return []
    return data[1]


def get_bbt_leaderboard(guild_id: int, date: datetime):
    data, c = supabaseClient.rpc(
        "get_bubble_tea_counts",
        {
            "guild_id": guild_id,
            "date": str(date),
        },
    ).execute()
    if c == 0:
        return []
    results = data[1]
    # sort the data
    results.sort(key=lambda x: x["count"], reverse=True)
    return results
