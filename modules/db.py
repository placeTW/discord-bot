import os
import psycopg2
import psycopg2.pool
import psycopg2.extras
from contextlib import contextmanager

_pool = psycopg2.pool.ThreadedConnectionPool(
    minconn=1,
    maxconn=5,
    user=os.getenv("POSTGRES_USER", "botuser"),
    password=os.getenv("POSTGRES_PASSWORD", ""),
    host=os.getenv("POSTGRES_HOST", "localhost"),
    port=os.getenv("POSTGRES_PORT", "5432"),
    dbname=os.getenv("POSTGRES_DB", "discord_bot"),
)


@contextmanager
def get_cursor():
    conn = _pool.getconn()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            yield cur
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        _pool.putconn(conn)


def close_pool():
    _pool.closeall()
