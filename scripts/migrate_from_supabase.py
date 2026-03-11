"""
One-shot CLI migration script: imports exported Supabase CSVs into the local PostgreSQL database.

The core migration logic lives in commands/migrate/migrate_cmd.py and is shared with
the /migrate Discord command.

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

import sys
from pathlib import Path

# Allow imports from the project root
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv

load_dotenv()

from commands.migrate.migrate_cmd import _run_migration


def main():
    print("Starting migration...\n")
    results = _run_migration()
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
