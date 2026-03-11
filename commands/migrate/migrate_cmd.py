import asyncio
import csv
import json
from pathlib import Path

import discord
import psycopg2.extras
from discord import app_commands

MIGRATION_DIR = Path(__file__).parent.parent.parent / "migration"

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


def _coerce_row(row: dict) -> dict:
    result = {}
    for k, v in row.items():
        if v == "" or v is None:
            result[k] = None
        elif k in JSONB_COLUMNS:
            try:
                result[k] = json.loads(v) if v else None
            except json.JSONDecodeError:
                result[k] = v
        elif k in BIGINT_COLUMNS:
            try:
                result[k] = int(v)
            except (ValueError, TypeError):
                result[k] = None
        else:
            result[k] = v
    return result


def _run_migration() -> list[tuple[str, int, str | None]]:
    """
    Runs the full migration synchronously.
    Returns a list of (table, rows_inserted, error_or_None) tuples.
    """
    from modules.db import get_cursor

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


def register_commands(tree: discord.app_commands.CommandTree, guild: discord.Object):
    @tree.command(
        name="migrate",
        description="Import Supabase CSV exports into the local database (admin only)",
        guild=guild,
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def migrate(interaction: discord.Interaction):
        if not interaction.permissions.administrator:
            await interaction.response.send_message(
                "You do not have the required permissions to use this command.", ephemeral=True
            )
            return

        await interaction.response.defer(ephemeral=True, thinking=True)

        results = await asyncio.to_thread(_run_migration)

        embed = discord.Embed(title="Migration Results", color=discord.Color.green())
        all_ok = True
        for table, count, error in results:
            if error:
                embed.add_field(name=f"❌ {table}", value=error, inline=False)
                all_ok = False
            else:
                embed.add_field(name=f"✅ {table}", value=f"{count} rows inserted", inline=False)

        if not all_ok:
            embed.color = discord.Color.orange()
            embed.set_footer(text="Some tables had errors. Check the logs for details.")
        else:
            embed.set_footer(text="Migration complete.")

        await interaction.followup.send(embed=embed, ephemeral=True)
