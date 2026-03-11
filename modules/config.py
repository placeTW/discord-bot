from modules.db import get_cursor


def fetch_configs(is_prod: bool):
    with get_cursor() as cur:
        cur.execute("SELECT * FROM server_config WHERE prod_config = %s", (is_prod,))
        rows = cur.fetchall()
    return {row['guild_id']: {k: v for k, v in row.items() if k != 'guild_id'} for row in rows}


def fetch_guild_config(guild_id: int, is_prod: bool):
    with get_cursor() as cur:
        cur.execute(
            "SELECT * FROM server_config WHERE guild_id = %s AND prod_config = %s",
            (guild_id, is_prod),
        )
        row = cur.fetchone()
    return dict(row) if row else {}


def create_new_config(guild_id: int, server_name: str, is_prod: bool):
    with get_cursor() as cur:
        cur.execute(
            "INSERT INTO server_config (guild_id, server_name, prod_config) VALUES (%s, %s, %s) RETURNING *",
            (guild_id, server_name, is_prod),
        )
        return cur.fetchall()


def set_config(guild_id: int, key: str, value: str, is_prod: bool) -> list:
    with get_cursor() as cur:
        cur.execute(
            f"UPDATE server_config SET {key} = %s WHERE guild_id = %s AND prod_config = %s RETURNING *",
            (value, guild_id, is_prod),
        )
        return cur.fetchall()


def remove_config(guild_id: int, is_prod: bool) -> list:
    with get_cursor() as cur:
        cur.execute(
            "DELETE FROM server_config WHERE guild_id = %s AND prod_config = %s RETURNING *",
            (guild_id, is_prod),
        )
        return cur.fetchall()
