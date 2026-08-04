"""Consolidated idempotent database seeder for SARAT NARAK.

Safe to run multiple times against any database — uses ON CONFLICT / existence
checks to skip existing rows without duplicating data.
"""

import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from src.database import get_supabase_client


def seed_all():
    client = get_supabase_client()
    print("=== Seeding Initial Data ===")

    # 1. Seed Profile row
    print("1. Seeding Profile...")
    profile_res = client.table("profile").select("id").execute()
    if not profile_res.data:
        client.table("profile").insert({
            "first_name": "Sarat",
            "last_name": "Narak",
            "hero_pitch": "I build backend APIs, mobile apps, and web dashboards — and this site is one of my projects too.",
            "tagline": "IT Student & Full-Stack Developer",
            "about_text": "I am an Information Technology student passionate about software engineering, backend systems, and clean UI design.",
            "about_bullets": ["Backend API Development", "Cross-Platform Mobile Apps", "Modern Web Interfaces"],
        }).execute()
        print("  -> Profile seeded.")
    else:
        print("  -> Profile already exists. Skipped.")

    # 2. Seed Stats
    print("2. Seeding Stats...")
    stats_data = [
        {"label": "Years Experience", "value": "2+", "icon_name": "Clock", "display_order": 1},
        {"label": "Projects Built", "value": "12+", "icon_name": "FolderGit2", "display_order": 2},
        {"label": "Tech Stack Items", "value": "15+", "icon_name": "Layers", "display_order": 3},
        {"label": "Code Commits", "value": "500+", "icon_name": "GitCommit", "display_order": 4},
    ]
    for stat in stats_data:
        res = client.table("stats").select("id").eq("label", stat["label"]).execute()
        if not res.data:
            client.table("stats").insert(stat).execute()
            print(f"  -> Stat '{stat['label']}' inserted.")
        else:
            print(f"  -> Stat '{stat['label']}' exists.")

    # 3. Seed Tech Stack
    print("3. Seeding Tech Stack...")
    tech_stack_items = [
        {"name": "Python", "icon_url": None, "display_order": 1},
        {"name": "FastAPI", "icon_url": None, "display_order": 2},
        {"name": "Nuxt 3", "icon_url": None, "display_order": 3},
        {"name": "Vue.js", "icon_url": None, "display_order": 4},
        {"name": "TypeScript", "icon_url": None, "display_order": 5},
        {"name": "PostgreSQL", "icon_url": None, "display_order": 6},
        {"name": "Supabase", "icon_url": None, "display_order": 7},
        {"name": "Tailwind CSS", "icon_url": None, "display_order": 8},
        {"name": "Flutter", "icon_url": None, "display_order": 9},
        {"name": "Git", "icon_url": None, "display_order": 10},
    ]
    for item in tech_stack_items:
        res = client.table("tech_stack").select("id").eq("name", item["name"]).execute()
        if not res.data:
            client.table("tech_stack").insert(item).execute()
            print(f"  -> Tech stack '{item['name']}' inserted.")
        else:
            print(f"  -> Tech stack '{item['name']}' exists.")

    # 4. Seed Skill Categories
    print("4. Seeding Skill Categories...")
    skill_categories_data = [
        {
            "name": "Backend Development",
            "icon_name": "Server",
            "items": ["FastAPI REST APIs", "Pydantic Schemas", "Supabase & PostgreSQL", "Auth & RBAC"],
            "display_order": 1,
        },
        {
            "name": "Frontend Engineering",
            "icon_name": "LayoutGrid",
            "items": ["Nuxt 3 & Vue 3", "Tailwind CSS Design Systems", "TypeScript", "Responsive UI"],
            "display_order": 2,
        },
        {
            "name": "Mobile Development",
            "icon_name": "Smartphone",
            "items": ["Flutter & Dart", "Android Native Apps", "Cross-Platform UI", "REST Integration"],
            "display_order": 3,
        },
        {
            "name": "Database & Infrastructure",
            "icon_name": "Database",
            "items": ["PostgreSQL Schema Design", "Supabase Auth & RLS", "FastAPI Cloud", "Vercel Hosting"],
            "display_order": 4,
        },
    ]
    for cat in skill_categories_data:
        res = client.table("skill_categories").select("id").eq("name", cat["name"]).execute()
        if not res.data:
            client.table("skill_categories").insert(cat).execute()
            print(f"  -> Skill Category '{cat['name']}' inserted.")
        else:
            print(f"  -> Skill Category '{cat['name']}' exists.")

    # 5. Seed Social Media
    print("5. Seeding Social Media Links...")
    social_media_data = [
        {"name": "GitHub", "value": "@saratnarak", "url": "https://github.com", "icon_url": None, "display_order": 1},
        {"name": "LinkedIn", "value": "Sarat Narak", "url": "https://linkedin.com", "icon_url": None, "display_order": 2},
        {"name": "Email", "value": "admin@saratnarak.com", "url": "mailto:admin@saratnarak.com", "icon_url": None, "display_order": 3},
    ]
    for social in social_media_data:
        res = client.table("social_media").select("id").eq("name", social["name"]).execute()
        if not res.data:
            client.table("social_media").insert(social).execute()
            print(f"  -> Social link '{social['name']}' inserted.")
        else:
            print(f"  -> Social link '{social['name']}' exists.")

    print("=== Seeding Completed Successfully ===")


if __name__ == "__main__":
    seed_all()
