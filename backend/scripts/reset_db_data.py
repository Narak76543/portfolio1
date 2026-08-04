"""Reset all database tables in Supabase and optionally re-seed initial data.

Usage:
    python scripts/reset_db_data.py [--force] [--seed]
"""

import sys
import argparse
from pathlib import Path

# Add backend directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.database import get_supabase_client
from scripts.seed_initial_data import seed_data


def reset_database(reseed: bool = True) -> None:
    """Clear all records from public tables in correct dependency order."""
    supabase = get_supabase_client()
    
    tables_in_order = [
        "qr_login_requests",
        "trusted_devices",
        "projects",
        "tech_stack",
        "stats",
        "social_media",
        "skill_categories",
        "profile",
    ]
    
    print("🧹 Cleaning database tables...")
    for table in tables_in_order:
        try:
            # Delete all rows by targeting non-null primary keys
            res = supabase.table(table).delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
            count = len(res.data) if res.data else 0
            print(f"  - Cleared {table} ({count} rows deleted)")
        except Exception as err:
            print(f"  ⚠️ Warning clearing {table}: {err}")

    print("✨ Database reset complete!")

    if reseed:
        print("\n🌱 Re-seeding clean initial data...")
        seed_data()
        print("✅ Initial data re-seeded successfully!")


def main() -> None:
    parser = argparse.ArgumentParser(description="Reset all database tables in Supabase.")
    parser.add_argument("--force", action="store_true", help="Skip confirmation prompt")
    parser.add_argument("--no-seed", action="store_true", help="Do not re-seed initial data after reset")
    args = parser.parse_args()

    if not args.force:
        confirm = input("⚠️ WARNING: This will delete ALL data in your Supabase database. Are you sure? (y/N): ").strip().lower()
        if confirm != "y":
            print("Operation cancelled.")
            sys.exit(0)

    reset_database(reseed=not args.no_seed)


if __name__ == "__main__":
    main()
