import datetime

from psycopg2 import sql

from modules.db import get_cursor

TABLE = "bubble_tea_entries"
_TABLE_ID = sql.Identifier(TABLE)

ALLOWED_BBT_COLUMNS = frozenset({
    "created_at", "user_id", "guild_id",
    "location", "description", "price", "currency", "image", "notes", "rating",
})


# Adds a new bubble tea entry to the database
def add_bbt_entry(created_at: datetime, user_id: int, guild_id: int, **kwargs):
    invalid = set(kwargs.keys()) - ALLOWED_BBT_COLUMNS
    if invalid:
        raise ValueError(f"Invalid column(s) for bubble_tea_entries: {invalid}")
    columns = ["created_at", "user_id", "guild_id"] + list(kwargs.keys())
    values = [str(created_at), user_id, guild_id] + list(kwargs.values())
    col_sql = sql.SQL(", ").join(sql.Identifier(c) for c in columns)
    placeholders_sql = sql.SQL(", ").join(sql.Placeholder() for _ in columns)
    with get_cursor() as cur:
        cur.execute(
            sql.SQL("INSERT INTO {} ({}) VALUES ({}) RETURNING id").format(
                _TABLE_ID, col_sql, placeholders_sql
            ),
            values,
        )
        row = cur.fetchone()
    return row["id"]


# Removes a bubble tea entry from the database by id
def remove_bbt_entry(id: int, user_id: int):
    with get_cursor() as cur:
        cur.execute(
            sql.SQL("DELETE FROM {} WHERE id = %s AND user_id = %s").format(_TABLE_ID),
            (id, user_id),
        )


# Gets a bubble tea entry from the database by id
def get_bbt_entry(id: int) -> dict | None:
    with get_cursor() as cur:
        cur.execute(
            sql.SQL("SELECT * FROM {} WHERE id = %s").format(_TABLE_ID),
            (id,),
        )
        row = cur.fetchone()
    return dict(row) if row else None


# Edits a bubble tea entry in the database by id
def edit_bbt_entry(id: int, owner_user_id: int, **kwargs):
    if not kwargs:
        return
    invalid = set(kwargs.keys()) - ALLOWED_BBT_COLUMNS
    if invalid:
        raise ValueError(f"Invalid column(s) for bubble_tea_entries: {invalid}")
    set_sql = sql.SQL(", ").join(
        sql.SQL("{} = %s").format(sql.Identifier(k)) for k in kwargs.keys()
    )
    values = list(kwargs.values()) + [id, owner_user_id]
    with get_cursor() as cur:
        cur.execute(
            sql.SQL("UPDATE {} SET {} WHERE id = %s AND user_id = %s").format(_TABLE_ID, set_sql),
            values,
        )


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
            sql.SQL("SELECT * FROM {} WHERE user_id = %s AND created_at >= %s AND created_at <= %s ORDER BY created_at DESC").format(_TABLE_ID),
            (user_id, str(date_from), str(date_to)),
        )
        return cur.fetchall()


# Gets the top bubble tea drinkers up to a given date
def get_bbt_leaderboard(guild_id: int, date: datetime):
    with get_cursor() as cur:
        cur.execute(
            sql.SQL("""
            SELECT user_id, COUNT(*) AS count, AVG(rating) AS average_rating
            FROM {}
            WHERE guild_id = %s AND created_at <= %s
            GROUP BY user_id
            ORDER BY count DESC
            """).format(_TABLE_ID),
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
                sql.SQL("""
                SELECT
                    location,
                    currency,
                    ARRAY_AGG(COALESCE(price, 0)::float) AS prices_list,
                    AVG(rating)  AS average_rating,
                    MIN(rating)  AS minimum_rating,
                    MAX(rating)  AS maximum_rating
                FROM {}
                WHERE user_id = %s AND created_at >= %s AND created_at <= %s
                GROUP BY location, currency
                ORDER BY location, COUNT(*) DESC
                """).format(_TABLE_ID),
                (user_id, str(year_start), str(date)),
            )
            return cur.fetchall()
    else:
        with get_cursor() as cur:
            cur.execute(
                sql.SQL("""
                SELECT
                    currency,
                    ARRAY_AGG(COALESCE(price, 0)::float) AS prices_list,
                    AVG(rating)  AS average_rating,
                    MIN(rating)  AS minimum_rating,
                    MAX(rating)  AS maximum_rating
                FROM {}
                WHERE user_id = %s AND created_at >= %s AND created_at <= %s
                GROUP BY currency
                ORDER BY COUNT(*) DESC
                """).format(_TABLE_ID),
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
            sql.SQL("""
            SELECT
                EXTRACT(MONTH FROM created_at)::int AS month,
                COUNT(*)        AS entry_count,
                AVG(rating)     AS average_rating,
                MIN(rating)     AS minimum_rating,
                MAX(rating)     AS maximum_rating
            FROM {}
            WHERE user_id = %s AND created_at >= %s AND created_at <= %s
            GROUP BY month
            ORDER BY month
            """).format(_TABLE_ID),
            (user_id, str(year_start), str(date)),
        )
        return cur.fetchall()


# Get the user's latest bubble tea entry
def get_latest_bubble_tea_entry(user_id: int):
    with get_cursor() as cur:
        cur.execute(
            sql.SQL("SELECT * FROM {} WHERE user_id = %s ORDER BY created_at DESC LIMIT 1").format(_TABLE_ID),
            (user_id,),
        )
        row = cur.fetchone()
    return dict(row) if row else None
