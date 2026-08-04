"""Create or update admin account in Supabase Auth.

Usage:
    python scripts/create_admin_account.py --email admin@example.com --password YourSecretPassword
    or interactively:
    python scripts/create_admin_account.py
"""

import sys
import argparse
from pathlib import Path

# Add backend directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.database import get_supabase_client


def create_or_update_admin(email: str, password: str) -> None:
    """Create a new admin user in Supabase Auth or update password if exists."""
    supabase = get_supabase_client()
    
    print(f"Creating admin account for: {email}...")
    try:
        user = supabase.auth.admin.create_user({
            "email": email,
            "password": password,
            "email_confirm": True,
        })
        print(f"✅ Admin user created successfully! User ID: {user.user.id}")
    except Exception as err:
        err_msg = str(err)
        if "already registered" in err_msg.lower() or "already exists" in err_msg.lower():
            print(f"ℹ️ User {email} already exists. Updating password...")
            # List users to find ID
            users = supabase.auth.admin.list_users()
            target_id = None
            for u in users:
                if u.email.lower() == email.lower():
                    target_id = u.id
                    break
            
            if target_id:
                supabase.auth.admin.update_user_by_id(target_id, {"password": password})
                print(f"✅ Password updated successfully for admin user ID: {target_id}")
            else:
                print(f"❌ Could not find user ID for {email}: {err}")
        else:
            print(f"❌ Failed to create admin user: {err}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Create or update Supabase Auth admin user.")
    parser.add_argument("--email", type=str, help="Admin user email")
    parser.add_argument("--password", type=str, help="Admin user password")
    args = parser.parse_args()

    email = args.email
    password = args.password

    if not email:
        email = input("Enter admin email address: ").strip()
    if not password:
        password = input("Enter admin password: ").strip()

    if not email or not password:
        print("❌ Email and password are required.")
        sys.exit(1)

    create_or_update_admin(email, password)


if __name__ == "__main__":
    main()
