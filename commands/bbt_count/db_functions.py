import datetime
from ..modules.supabase import supabaseClient

TABLE = "bubble_tea_entries"


# Adds a new bubble tea entry to the database
def add_bbt_entry(created_at: datetime, user_id: int, guild_id: int, **kwargs):
    response = (
        supabaseClient.table(TABLE)
        .insert(
            {
                "created_at": str(created_at),
                "user_id": user_id,
                "guild_id": guild_id,
                **kwargs,
            }
        )
        .execute()
    )
    print(response)
    return response.data[0]["id"]


# Removes a bubble tea entry from the database by id
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


# Gets a bubble tea entry from the database by id
def get_bbt_entry(id: int) -> dict | None:
    data, c = (
        supabaseClient.table(TABLE)
        .select("*")
        .match(
            {
                "id": id,
            }
        )
        .execute()
    )
    if c == 0:
        return None
    try:
        return data[1][0]
    except IndexError:
        return None


# Edits a bubble tea entry in the database by id
def edit_bbt_entry(id: int, owner_user_id: int, **kwargs):
    response = (
        supabaseClient.table(TABLE)
        .update(kwargs)
        .match(
            {
                "id": id,
                "user_id": owner_user_id,
            }
        )
        .execute()
    )
    print(response)


# Gets all bubble tea entries from the database for a user in a given year
def get_bbt_entries(user_id: int, year: int = None, page: int = 1):
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
        .range(page * 10, (page - 1) * 10)
        .execute()
    )
    if c == 0:
        return []
    return data[1]


# Gets the top bubble tea drinkers in a given year
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
    return results


# Gets the bubble tea stats for a user in a given year
def get_bubble_tea_stats(
    user_id: int, date: datetime, group_by_location=False
):
    data, c = supabaseClient.rpc(
        "get_bubble_tea_stats",
        {
            "user_id": user_id,
            "date": str(date),
            "group_by_location": group_by_location,
        },
    ).execute()
    if c == 0:
        return []
    results = data[1]
    return results


# Gets the bubble tea monthly counts for a user
def get_bubble_tea_monthly_counts(user_id: int, date: datetime):
    data, c = supabaseClient.rpc(
        "get_bubble_tea_monthly_counts",
        {
            "user_id": user_id,
            "date": str(date),
        },
    ).execute()
    if c == 0:
        return []
    results = data[1]
    return results


# Get the user's latest bubble tea entry
def get_latest_bubble_tea_entry(user_id: int):
    data, c = (
        supabaseClient.table(TABLE)
        .select("*")
        .match(
            {
                "user_id": user_id,
            }
        )
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )
    if c == 0:
        return None
    try:
        return data[1][0]
    except IndexError:
        return None
