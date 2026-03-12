from modules.db import get_cursor
from random import randint

TABLE = "tocfl"


def get_random_tocfl_word(level: int | None = None) -> dict | None:
    with get_cursor() as cur:
        if level is not None:
            cur.execute(
                "SELECT * FROM tocfl WHERE level = %s ORDER BY RANDOM() LIMIT 1",
                (level,),
            )
        else:
            cur.execute("SELECT MAX(id) FROM tocfl")
            max_row = cur.fetchone()
            max_id = max_row["max"] if max_row and max_row["max"] else 1
            random_id = randint(1, max_id)
            cur.execute("SELECT * FROM tocfl WHERE id = %s", (random_id,))
        row = cur.fetchone()
    return dict(row) if row else None


def get_random_tocfl_choices_from_db(num_choices=5):
    with get_cursor() as cur:
        cur.execute(
            "SELECT DISTINCT ON (pinyin) * FROM tocfl ORDER BY pinyin, RANDOM() LIMIT %s",
            (num_choices,),
        )
        rows = cur.fetchall()
    return rows if rows else None


if __name__ == "__main__":
    choices = get_random_tocfl_choices_from_db()
    print(choices)
