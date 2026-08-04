-- ==============================================================================
-- SARAT NARAK — Supabase SQL Master Schema Reference (FROZEN SNAPSHOT)
-- ==============================================================================
-- NOTE: This file serves as a frozen historical reference of the full database schema.
-- The canonical, authoritative source of truth for database migrations is managed by
-- Alembic under `backend/alembic/versions/`.
-- ==============================================================================

-- 1. Projects Table
CREATE TABLE IF NOT EXISTS projects (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL,
  slug TEXT UNIQUE NOT NULL,
  short_description TEXT,
  full_description TEXT,
  tech_stack TEXT[] DEFAULT '{}',
  role TEXT,
  github_url TEXT,
  live_url TEXT,
  cover_image_url TEXT,
  featured BOOLEAN DEFAULT FALSE,
  display_order INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_projects_slug ON projects (slug);
CREATE INDEX IF NOT EXISTS idx_projects_featured_created ON projects (featured DESC, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_projects_order ON projects (display_order ASC);

-- 2. Profile Table
CREATE TABLE IF NOT EXISTS profile (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tagline TEXT,
  first_name TEXT,
  last_name TEXT,
  hero_pitch TEXT,
  about_text TEXT,
  about_bullets TEXT[] DEFAULT '{}',
  custom_logo_url TEXT,
  heading_font_url TEXT,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- 3. Stats Table
CREATE TABLE IF NOT EXISTS stats (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  label TEXT NOT NULL,
  value TEXT NOT NULL,
  icon_name TEXT NOT NULL,
  display_order INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_stats_order ON stats (display_order ASC);

-- 4. Social Media Table
CREATE TABLE IF NOT EXISTS social_media (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  value TEXT NOT NULL,
  url TEXT NOT NULL,
  icon_url TEXT,
  display_order INTEGER NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_social_media_order ON social_media (display_order ASC);

-- 5. Tech Stack Table
CREATE TABLE IF NOT EXISTS tech_stack (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  icon_url TEXT,
  display_order INTEGER NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_tech_stack_order ON tech_stack (display_order ASC);

-- 6. Skill Categories Table
CREATE TABLE IF NOT EXISTS skill_categories (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  icon_name TEXT NOT NULL,
  items TEXT[] NOT NULL DEFAULT '{}',
  display_order INTEGER NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_skill_categories_order ON skill_categories (display_order ASC);

-- 7. Trusted Devices Table (QR Auth)
CREATE TABLE IF NOT EXISTS trusted_devices (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  device_secret_hash TEXT NOT NULL UNIQUE,
  device_label TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now(),
  last_used_at TIMESTAMPTZ DEFAULT now()
);

-- 8. QR Login Requests Table (QR Auth)
CREATE TABLE IF NOT EXISTS qr_login_requests (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  status TEXT NOT NULL DEFAULT 'pending',
  expires_at TIMESTAMPTZ NOT NULL,
  approved_by_device_id UUID REFERENCES trusted_devices(id) ON DELETE SET NULL,
  access_token TEXT,
  refresh_token TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_qr_login_requests_status ON qr_login_requests (status);
