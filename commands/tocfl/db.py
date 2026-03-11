from modules.db import get_cursor

TABLE = "tocfl"


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
