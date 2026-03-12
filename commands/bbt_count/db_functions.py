import datetime

from modules.db import get_cursor

TABLE = "bubble_tea_entries"


# Adds a new bubble tea entry to the database
def add_bbt_entry(created_at: datetime, user_id: int, guild_id: int, **kwargs):
    columns = ["created_at", "user_id", "guild_id"] + list(kwargs.keys())
    values = [str(created_at), user_id, guild_id] + list(kwargs.values())
    placeholders = ", ".join(["%s"] * len(columns))
    col_list = ", ".join(columns)
    with get_cursor() as cur:
        cur.execute(
            f"INSERT INTO {TABLE} ({col_list}) VALUES ({placeholders}) RETURNING id",
            values,
        )
        row = cur.fetchone()
    print(row)
    return row["id"]


# Removes a bubble tea entry from the database by id
def remove_bbt_entry(id: int, user_id: int):
    with get_cursor() as cur:
        cur.execute(f"DELETE FROM {TABLE} WHERE id = %s AND user_id = %s", (id, user_id))
    print(f"Removed entry {id}")


# Gets a bubble tea entry from the database by id
def get_bbt_entry(id: int) -> dict | None:
    with get_cursor() as cur:
        cur.execute(f"SELECT * FROM {TABLE} WHERE id = %s", (id,))
        row = cur.fetchone()
    return dict(row) if row else None


# Edits a bubble tea entry in the database by id
def edit_bbt_entry(id: int, owner_user_id: int, **kwargs):
    if not kwargs:
        return
    set_clause = ", ".join([f"{k} = %s" for k in kwargs.keys()])
    values = list(kwargs.values()) + [id, owner_user_id]
    with get_cursor() as cur:
        cur.execute(
            f"UPDATE {TABLE} SET {set_clause} WHERE id = %s AND user_id = %s",
            values,
        )
    print(f"Updated entry {id}")


# Gets all bubble tea entries from the database for a user in a given year
def get_bbt_entries(user_id: int, year: int = None):
    if year is None:
        date_from = datetime.datetime.now() - datetime.timedelta(days=365)
        date_to = datetime.datetime.now() + datetime.timedelta(days=1)
    else:
        date_from = datetime.datetime(year, 1, 1)
        date_to = datetime.datetime(year, 12, 31)
    with get_cursor() as cur:
        cur.execute(
            f"SELECT * FROM {TABLE} WHERE user_id = %s AND created_at >= %s AND created_at <= %s ORDER BY created_at DESC",
            (user_id, str(date_from), str(date_to)),
        )
        return cur.fetchall()


# Gets the top bubble tea drinkers up to a given date
def get_bbt_leaderboard(guild_id: int, date: datetime):
    with get_cursor() as cur:
        cur.execute(
            f"""
            SELECT user_id, COUNT(*) AS count, AVG(rating) AS average_rating
            FROM {TABLE}
            WHERE guild_id = %s AND created_at <= %s
            GROUP BY user_id
            ORDER BY count DESC
            """,
            (guild_id, str(date)),
        )
        return cur.fetchall()


# Gets the bubble tea stats for a user in a given year.
# Returns rows grouped by currency (and optionally location), each with a prices_list array
# and rating aggregates — matching the shape expected by bbt_stats_embed.
def get_bubble_tea_stats(user_id: int, date: datetime, group_by_location=False):
    year_start = datetime.datetime(date.year, 1, 1)
    if group_by_location:
        with get_cursor() as cur:
            cur.execute(
                f"""
                SELECT
                    location,
                    currency,
                    ARRAY_AGG(COALESCE(price, 0)::float) AS prices_list,
                    AVG(rating)  AS average_rating,
                    MIN(rating)  AS minimum_rating,
                    MAX(rating)  AS maximum_rating
                FROM {TABLE}
                WHERE user_id = %s AND created_at >= %s AND created_at <= %s
                GROUP BY location, currency
                ORDER BY location, COUNT(*) DESC
                """,
                (user_id, str(year_start), str(date)),
            )
            return cur.fetchall()
    else:
        with get_cursor() as cur:
            cur.execute(
                f"""
                SELECT
                    currency,
                    ARRAY_AGG(COALESCE(price, 0)::float) AS prices_list,
                    AVG(rating)  AS average_rating,
                    MIN(rating)  AS minimum_rating,
                    MAX(rating)  AS maximum_rating
                FROM {TABLE}
                WHERE user_id = %s AND created_at >= %s AND created_at <= %s
                GROUP BY currency
                ORDER BY COUNT(*) DESC
                """,
                (user_id, str(year_start), str(date)),
            )
            return cur.fetchall()


# Gets the bubble tea monthly counts for a user in the same year as date.
# Returns rows with integer month, entry_count, and rating aggregates
# matching the shape expected by bbt_stats_embed.
def get_bubble_tea_monthly_counts(user_id: int, date: datetime):
    year_start = datetime.datetime(date.year, 1, 1)
    with get_cursor() as cur:
        cur.execute(
            f"""
            SELECT
                EXTRACT(MONTH FROM created_at)::int AS month,
                COUNT(*)        AS entry_count,
                AVG(rating)     AS average_rating,
                MIN(rating)     AS minimum_rating,
                MAX(rating)     AS maximum_rating
            FROM {TABLE}
            WHERE user_id = %s AND created_at >= %s AND created_at <= %s
            GROUP BY month
            ORDER BY month
            """,
            (user_id, str(year_start), str(date)),
        )
        return cur.fetchall()


# Get the user's latest bubble tea entry
def get_latest_bubble_tea_entry(user_id: int):
    with get_cursor() as cur:
        cur.execute(
            f"SELECT * FROM {TABLE} WHERE user_id = %s ORDER BY created_at DESC LIMIT 1",
            (user_id,),
        )
        row = cur.fetchone()
    return dict(row) if row else None
