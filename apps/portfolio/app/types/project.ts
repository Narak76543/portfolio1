/** Mirrors the backend ProjectResponse schema field-for-field. */
export interface Project {
  id: string
  title: string
  slug: string
  short_description: string | null
  full_description: string | null
  tech_stack: string[]
  role: string | null
  github_url: string | null
  live_url: string | null
  cover_image_url: string | null
  featured: boolean
  created_at: string
}

/** Used when creating a new project via the admin panel. */
export interface ProjectCreate {
  title: string
  slug: string
  short_description?: string | null
  full_description?: string | null
  tech_stack?: string[]
  role?: string | null
  github_url?: string | null
  live_url?: string | null
  cover_image_url?: string | null
  featured?: boolean
}

/** Used when updating a project via the admin panel. */
export interface ProjectUpdate {
  title?: string
  slug?: string
  short_description?: string | null
  full_description?: string | null
  tech_stack?: string[]
  role?: string | null
  github_url?: string | null
  live_url?: string | null
  cover_image_url?: string | null
  featured?: boolean
}
