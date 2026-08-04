export interface SocialMediaItem {
  id: string
  name: string
  value: string
  url: string
  icon_url?: string | null
  display_order: number
  created_at?: string
}

export interface SocialMediaCreate {
  name: string
  value: string
  url: string
  icon_url?: string | null
  display_order?: number
}

export interface SocialMediaUpdate {
  name?: string
  value?: string
  url?: string
  icon_url?: string | null
  display_order?: number
}
