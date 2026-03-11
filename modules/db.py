import os
import psycopg2
import psycopg2.pool
import psycopg2.extras
from contextlib import contextmanager
from dotenv import load_dotenv

load_dotenv()

# Accept either a full DATABASE_URL or individual POSTGRES_* vars
_dsn = os.getenv("DATABASE_URL") or (
    "postgresql://{user}:{password}@{host}:{port}/{db}".format(
        user=os.getenv("POSTGRES_USER", "botuser"),
        password=os.getenv("POSTGRES_PASSWORD", ""),
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        db=os.getenv("POSTGRES_DB", "discord_bot"),
    )
)

_pool = psycopg2.pool.ThreadedConnectionPool(
    minconn=1,
    maxconn=5,
    dsn=_dsn,
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
