# SARAT NARAK — Portfolio Website Content Draft

> This document is the full content/copy for the portfolio site, ready to hand off to your build agent (Antigravity). Tech stack: **Nuxt** (frontend), **FastAPI** (backend/API), **Supabase/PostgreSQL** (database + auth for admin).

---

## 1. Site Identity

- **Site name:** SARAT NARAK
- **Tagline (hero subtitle):** "IT Student & Full-Stack Developer — Building with FastAPI, Flutter, Nuxt & Supabase"
- **One-line pitch (for meta description / About preview):** "I'm an IT student who builds full-stack applications — from mobile apps to backend APIs — and this portfolio itself is one of my projects."

---

## 2. Hero Section

```
SARAT NARAK
IT Student · Full-Stack Developer

I build backend APIs, mobile apps, and web dashboards —
and this site is one of my projects too.

[View Projects]   [Contact Me]   [Download Resume]
```

---

## 3. About Section

**Heading:** About Me

**Body copy (draft — replace bracketed info with your real details):**

> I'm an IT student focused on full-stack development, working across backend, frontend, and mobile. My core stack is **FastAPI** for building APIs, **Flutter** for mobile apps, **Nuxt** for web frontends, and **PostgreSQL/Supabase** for data and authentication.
>
> I'm currently looking for a junior/entry-level IT role where I can keep building real products and grow as a developer. This portfolio itself — **SARAT NARAK** — is built with my own stack, including an admin panel I built myself so I can manage and update my projects without touching code every time.

**Quick facts (optional sidebar):**
- 🎓 IT Student
- 💻 Stack: FastAPI · Flutter · Nuxt · Supabase/PostgreSQL
- 📍 Based in [your city]
- 🎯 Looking for: Junior/Entry-level IT roles

---

## 4. Featured Project — SARAT NARAK (this site)

**This is your flagship project entry — feature it first/prominently.**

- **Name:** SARAT NARAK (This Portfolio)
- **What it does:** A full-stack portfolio website with a built-in admin panel — I can log in and add, edit, or remove projects at any time without redeploying code.
- **Stack:**
  - Nuxt — public-facing site (SSR for SEO, fast load)
  - FastAPI — backend API serving project data, handling admin auth
  - Supabase/PostgreSQL — stores project entries, images, and admin credentials
- **Key feature to highlight:** Admin CMS — protected `/admin` route with login, CRUD interface for projects (title, description, tech stack tags, GitHub link, live demo link, images)
- **Why it matters for interviews:** Shows you can design a database schema, build a REST API, secure an admin route with auth, and ship a real deployed product — not just a template.
- **Links:** [Live site] · [GitHub repo]

---

## 5. Other Projects (from your GitHub — pinned repos)

> ⚠️ These descriptions are drafted from repo names only, since you asked me to guess. **Please correct/fill in the real details before publishing** — especially the "what it does" and "your role" lines, which I can't know from the name alone.

### bots_telegram_assignment
- **What it does (guess):** A Telegram bot built as a coursework/assignment project — likely handles user commands and automated responses.
- **Stack:** Python
- **Your role:** _[fill in — solo/team, what you specifically built]_
- **Link:** https://github.com/Narak76543/bots_telegram_assignment

### dashboard_web_vue
- **What it does (guess):** A web dashboard interface — likely displays data/analytics in a Vue-based UI.
- **Stack:** Vue
- **Your role:** _[fill in]_
- **Link:** https://github.com/Narak76543/dashboard_web_vue

### fast_api_best_practice
- **What it does (guess):** A reference/practice project demonstrating FastAPI best practices — project structure, routing, possibly auth or DB patterns.
- **Stack:** FastAPI (Python)
- **Your role:** _[fill in]_
- **Link:** https://github.com/Narak76543/fast_api_best_practice

### kh_driving_rule_app
- **What it does (guess):** A mobile app related to Cambodian ("KH") driving rules — likely a study/reference app for driving test rules.
- **Stack:** Dart (Flutter)
- **Your role:** _[fill in]_
- **Link:** https://github.com/Narak76543/kh_driving_rule_app

### hcph_backend
- **What it does (guess):** Backend/API service for a project abbreviated "HCPH" — possibly healthcare-related.
- **Stack:** Python
- **Your role:** _[fill in]_
- **Link:** https://github.com/Narak76543/hcph_backend

### hcph_mobile
- **What it does (guess):** Companion mobile app for the "HCPH" project above.
- **Stack:** Dart (Flutter)
- **Your role:** _[fill in]_
- **Link:** https://github.com/Narak76543/hcph_mobile

> Note: your GitHub shows **49 repositories total** — these 6 are just your pinned ones. If you have other strong projects not pinned, let me know and I'll add them too.

---

## 6. Skills Section

**Backend**
- FastAPI (Python)
- REST API design
- PostgreSQL

**Frontend**
- Nuxt / Vue
- HTML, CSS, JavaScript

**Mobile**
- Flutter (Dart)

**Database & Infra**
- Supabase (Auth, Database, Storage)
- PostgreSQL

**Tools**
- Git / GitHub
- _[add: Docker, Postman, VS Code, etc. — whatever you actually use]_

---

## 7. Admin CMS — Feature Spec (for Antigravity to build)

This is the functional spec for the admin panel, since you said "allow me to input later from web admin":

**Auth:**
- Login page at `/admin/login`
- Supabase Auth (email/password) — only your account has access

**Admin Dashboard (`/admin/projects`):**
- List all projects (table view)
- "Add Project" button → form with fields:
  - Title
  - Short description
  - Full description (rich text or markdown)
  - Tech stack tags (multi-select or comma-separated)
  - Your role
  - GitHub link
  - Live demo link (optional)
  - Cover image upload (Supabase Storage)
  - Featured toggle (to pin it to top, like SARAT NARAK entry)
- Edit / Delete existing projects

**Public site:**
- `/projects` — fetches project list from FastAPI → Supabase, renders as cards
- `/projects/[slug]` — individual project detail page

**Suggested DB table (Supabase/PostgreSQL):**
```sql
create table projects (
  id uuid primary key default gen_random_uuid(),
  title text not null,
  slug text unique not null,
  short_description text,
  full_description text,
  tech_stack text[], -- array of tags
  role text,
  github_url text,
  live_url text,
  cover_image_url text,
  featured boolean default false,
  created_at timestamp default now()
);
```

---

## 8. Contact Section

**Heading:** Let's Connect

```
Open to junior/entry-level IT roles.

📧 [your email]
💻 GitHub: github.com/Narak76543
🔗 LinkedIn: [your link]
📄 [Download Resume]
```

---

## Next Steps

1. Fill in the `[bracketed]` placeholders above (real bio details, actual project descriptions, your role on each repo, contact info).
2. Correct or confirm the guessed project descriptions — especially "what it does" and "your role."
3. Hand this file to Antigravity along with the Admin CMS spec (Section 7) to scaffold the Nuxt + FastAPI + Supabase project.
4. Once the site is live, I can help you write a matching resume/PDF version, or review the deployed site's copy and SEO.
