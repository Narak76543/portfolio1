# AGENTS.md — SARAT NARAK Project Standards

## Project: SARAT NARAK (Portfolio + Portfolio Admin)

## Stack
- **Frontend:** Nuxt 3 + Tailwind CSS (used for BOTH the public portfolio site and the portfolio admin panel)
- **Backend:** FastAPI + Python 3.11
- **Database/Auth:** Supabase (PostgreSQL, Auth, Storage)
- **Font:** Onest (used everywhere — headings, body, UI)
- **Design style:** Clean, modern, light mode only. No dark mode toggle needed.
- Package-by-feature (domain-driven) structure on the backend, not package-by-type

---

## Design System — MANDATORY, apply across both Portfolio and Portfolio Admin

**Design language: Samsung One UI.** This replaces all earlier low-border-radius/purple-accent/FastAPI-Cloud-dark-mode rules below — those are superseded.

### Typography
- Font family: `Onest` (Google Fonts, open-source, OFL licensed — chosen because it's explicitly designed with a Samsung One UI-inspired geometric feel, matching our design language), loaded via `@nuxt/fonts` or a `<link>` in `app.head`
- Never fall back to a different display font — Onest only, all weights (400/500/600/700) as needed
- Tailwind config must set Onest as `fontFamily.sans` so `font-sans` is Onest by default
- Exception: the name/heading text may use a custom uploaded font if one is set via the admin panel (see the font upload feature) — this does not apply to body/UI text, which stays Onest.

### One UI Design Tokens — MANDATORY, exact values

**Border radii:**
- Main focus blocks / container cards: `26px` radius (`rounded-[26px]` in Tailwind, or define as a `rounded-card` theme token set to `26px`)
- Buttons and navigation pills: fully rounded pill shape (`rounded-full` / `9999px`)
- This REPLACES the earlier low-border-radius rule — cards are now generously rounded, not sharp.

**Light mode palette:**
- Scaffold / page background: `#F2F4F7`
- Card / focus block background: `#FFFFFF`
- Primary text: `#101010`
- Secondary text: `#707070`
- Primary accent color: `#0381FE`

**Dark mode palette:**
- Scaffold / page background: `#000000` (OLED black)
- Card / focus block background: `#1C1C1E` (elevated surface)
- Primary text: `#F2F2F7`
- Secondary text: `#8E8E93`
- Primary accent color: `#0381FE` (same blue in both modes)

**This REPLACES:**
- The purple accent color — accent is now `#0381FE` blue everywhere (buttons, links, active states, icon backgrounds), in both light and dark mode.
- The FastAPI Cloud `zinc`-based dark mode palette — dark mode now uses true OLED black (`#000000`) for the page background and `#1C1C1E` for cards specifically, not `zinc-950`/`zinc-900`.
- The low-border-radius rule — cards now use `26px` radius, buttons/pills are fully rounded.

Define all five colors (per mode) and the `26px` card radius as Tailwind theme tokens (e.g. `background`, `surface`, `text-primary`, `text-secondary`, `primary` for accent, and `rounded-card` for the radius) so every component references the token, not a hardcoded hex/px value — this is required after the repeated inconsistency issues we hit with the previous color system.

### Visual style
- Light AND dark mode, with a toggle — same toggle mechanism as before (see implementation rules below), just new palette values.
- Cards should read as "elevated blocks" — on light mode use a subtle shadow (`shadow-sm`) since the white-on-`#F2F4F7` contrast is soft; on dark mode use the `#1C1C1E` surface color to create elevation against the pure black background (no shadow needed, OLED black doesn't show shadows well).
- Buttons are fully pill-shaped (`rounded-full`) with generous horizontal padding, per One UI convention.
- Generous whitespace and padding inside cards, consistent with One UI's spacious feel — don't cram content edge-to-edge inside the `26px`-radius containers.

### Dark mode implementation rules
- Use Tailwind's `dark:` variant class-based strategy (`darkMode: 'class'`), toggled by adding/removing a `dark` class on `<html>`.
- Store the user's preference (localStorage/cookie) so it persists across visits, no flash of wrong theme on load.
- Every component with a background, text, or border color MUST define both its light and `dark:` variant, using the theme tokens above — no component should look broken or unstyled in either mode.
- The toggle control goes in the nav bar, consistent across both `apps/portfolio` and `apps/portfolio-admin`.

### Rules — always follow (design)
- Never hardcode colors or font names directly in a component (`text-[#123456]`, `font-['Quicksand']`) — always reference the Tailwind theme tokens defined above.
- Never mix in a second font family for body/UI text, even for "just this one heading" (the name/heading custom-font exception is the only carve-out).
- Cards/containers use `26px` radius (the `rounded-card` token); buttons/pills use `rounded-full`. Nothing should still be using the old `rounded-sm`/`rounded-md` low-radius style or plain squared corners — that rule is superseded.
- Every new page must reuse existing shared components (Button, Card, Input, etc.) before creating a new one — check `components/ui/` first

---

## Frontend module structure — MANDATORY for Nuxt apps (Portfolio + Portfolio Admin)

Each Nuxt app (`portfolio/` and `portfolio-admin/`, or `apps/portfolio` and `apps/admin` in a monorepo) MUST follow this structure:

- `pages/` — route-level views only. No API calls or business logic inline — call composables.
- `components/` — reusable UI, grouped by feature (`components/project/`, `components/ui/`)
- `composables/` — data-fetching and shared logic (e.g. `useProjects.ts`, `useAuth.ts`)
- `layouts/` — shared page shells (`default.vue`, `admin.vue`)
- `types/` — shared TypeScript types/interfaces, mirroring backend schemas
- `utils/` — pure helper functions only, no API calls
- `assets/css/` — Tailwind config + Onest font import

### Rules — always follow (frontend)
- Never call `fetch`/`$fetch` directly inside a `.vue` component — always go through a composable
- Never duplicate a type — if the backend schema defines `Project`, the frontend `types/project.ts` must mirror it field-for-field
- Admin pages must live under a distinct route prefix (e.g. `/admin/*`) and use the `admin` layout, never the public `default` layout
- Every form on the admin panel must show loading and error states — no silent failures

---

## Backend domain module structure — MANDATORY for every domain (e.g. project/, auth/)

Every domain folder MUST contain exactly these files, no more no less unless justified:
- `router.py` — HTTP layer only. No DB queries, no business logic.
- `schemas.py` — Pydantic request/response models. Never expose models.py directly.
- `models.py` — SQLAlchemy or Supabase table models only.
- `service.py` — ALL business logic and DB queries live here.
- `dependencies.py` — FastAPI `Depends()` injectables (e.g. `get_current_admin`, `get_project_or_404`).
- `constants.py` — Error codes, enums, fixed values.
- `exceptions.py` — Custom exceptions inheriting from `src.exceptions.AppException`.
- `utils.py` — Pure helper functions only, no DB session, no request context.

## Rules — always follow (backend)
- Never put a raw `HTTPException` inline in `router.py` — always raise a custom exception from `exceptions.py`.
- Never query the DB directly in `router.py` — always go through `service.py`.
- Never return a raw DB row directly from a route — always map through a schema in `schemas.py`.
- Every new domain must be registered in `src/api.py`, never imported directly in `main.py`.
- Global settings only in `src/config.py` using `pydantic-settings`. Never hardcode env values (Supabase URL/keys included).
- `main.py` only contains app setup (middleware, CORS, exception handlers, lifespan) — never route logic or router imports besides `api_router`.
- Supabase service-role key is used ONLY on the backend, never exposed to the Nuxt frontend. Frontend uses the public anon key only, and only for auth session handling — all data reads/writes to `projects` go through FastAPI, not directly from Nuxt to Supabase.

---

## Naming
- `snake_case` for backend files and functions, `PascalCase` for backend classes
- `camelCase` for frontend variables/functions, `PascalCase` for Vue components
- Every custom exception ends in a descriptive noun (e.g. `ProjectNotFound`, not `NotFoundError`)

---

## Before finishing any task
- Confirm the backend domain still has exactly the 8 files listed above.
- Confirm both Nuxt apps (Portfolio, Portfolio Admin) use the One UI design tokens correctly — `26px` card radius, pill-shaped buttons, correct light/dark palette hex values, `#0381FE` accent — via theme tokens, not hardcoded values.
- Confirm any new admin form has loading/error states before marking the task done.
- Confirm no Supabase keys or secrets are committed or exposed client-side.

---

## Business context
- **Two apps, one backend:** Public Portfolio (read-only, public routes) and Portfolio Admin (auth-gated, CRUD routes) — both call the same FastAPI backend.
- **Auth:** Only the site owner has an account. Admin login via Supabase Auth (email/password), protected by a `get_current_admin` dependency on all admin routes.
- **Core entity — `Project`:** title, slug, short_description, full_description, tech_stack (array of tags), role, github_url, live_url, cover_image_url, featured (boolean), created_at.
- **Featured project rule:** exactly one project (SARAT NARAK itself) is pinned/featured by default and should always render first on the public site, but the `featured` flag must remain editable from the admin panel, not hardcoded.
- **Images:** uploaded via the admin panel to Supabase Storage, not stored as base64 in the DB — only the resulting URL is stored on the `Project` row.

## Type safety
Before considering any task complete, confirm there are zero type-checker warnings (basedpyright on the backend, `vue-tsc`/TypeScript on the frontend) on any file touched during that task. Do not leave known type errors "for later" — fix them as part of the same task, since they often indicate real bugs, not just style issues.