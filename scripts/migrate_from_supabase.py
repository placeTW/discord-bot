"""
One-shot CLI migration script: imports exported Supabase CSVs into the local PostgreSQL database.

Usage:
    python scripts/migrate_from_supabase.py

    Requires the following environment variables to be set (via .env file or shell):
        POSTGRES_HOST=localhost
        POSTGRES_PORT=5432
        POSTGRES_DB=discord_bot
        POSTGRES_USER=botuser
        POSTGRES_PASSWORD=password

Expects CSV files in the migration/ directory (exported from Supabase):
    migration/server_config_rows.csv
    migration/event_logs_rows.csv
    migration/message_logs_rows.csv
    migration/bubble_tea_entries_rows.csv
    migration/tocfl_rows.csv
"""

import csv
import json
import sys
from pathlib import Path

import psycopg2.extras
from dotenv import load_dotenv

# Allow imports from the project root
sys.path.insert(0, str(Path(__file__).parent.parent))

load_dotenv()

from modules.db import get_cursor

MIGRATION_DIR = Path(__file__).parent.parent / "migration"

TABLES = [
    "server_config",
    "event_logs",
    "message_logs",
    "bubble_tea_entries",
    "tocfl",
]

JSONB_COLUMNS = {"metadata", "confession_config", "confession_channels"}

BIGINT_COLUMNS = {
    "guild_id", "message_id", "author_id", "mentioned_id", "channel_id",
    "user_id", "confession_channel_id", "admin_role_id", "report_channel_id",
}

NUMERIC_COLUMNS = {"price", "rating"}


def _coerce_row(row: dict) -> dict:
    result = {}
    for k, v in row.items():
        if v == "" or v is None:
            result[k] = None
        elif k in JSONB_COLUMNS:
            try:
                result[k] = psycopg2.extras.Json(json.loads(v)) if v else None
            except json.JSONDecodeError:
                result[k] = v
        elif k in BIGINT_COLUMNS:
            try:
                result[k] = int(v)
            except (ValueError, TypeError):
                result[k] = None
        elif k in NUMERIC_COLUMNS:
            try:
                result[k] = float(v)
            except (ValueError, TypeError):
                result[k] = None
        else:
            result[k] = v
    return result


def run_migration() -> list[tuple[str, int, str | None]]:
    """
    Runs the full migration.
    Returns a list of (table, rows_inserted, error_or_None) tuples.
    """
    results = []
    for table in TABLES:
        csv_path = MIGRATION_DIR / f"{table}_rows.csv"
        if not csv_path.exists():
            results.append((table, 0, f"CSV not found at {csv_path}"))
            continue

        with open(csv_path, newline="", encoding="utf-8") as f:
            rows = [_coerce_row(row) for row in csv.DictReader(f)]

        if not rows:
            results.append((table, 0, "CSV is empty"))
            continue

        try:
            with get_cursor() as cur:
                columns = list(rows[0].keys())
                col_list = ", ".join(columns)
                placeholders = ", ".join([f"%({col})s" for col in columns])
                sql = f"INSERT INTO {table} ({col_list}) VALUES ({placeholders}) ON CONFLICT DO NOTHING"
                psycopg2.extras.execute_batch(cur, sql, rows)
                if "id" in columns:
                    cur.execute(
                        f"SELECT setval(pg_get_serial_sequence('{table}', 'id'), MAX(id)) FROM {table}"
                    )
            results.append((table, len(rows), None))
        except Exception as e:
            results.append((table, 0, str(e)))

    return results


def main():
    print("Starting migration...\n")
    results = run_migration()
    all_ok = True
    for table, count, error in results:
        if error:
            print(f"  ERROR {table}: {error}", file=sys.stderr)
            all_ok = False
        else:
            print(f"  OK    {table}: {count} rows inserted")

    if not all_ok:
        print("\nMigration completed with errors.", file=sys.stderr)
        sys.exit(1)
    else:
        print("\nMigration complete.")


if __name__ == "__main__":
    main()
