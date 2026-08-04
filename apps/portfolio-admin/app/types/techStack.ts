export interface TechStackItem {
  id: str
  name: str
  icon_url: str | null
  display_order: number
  created_at?: string
}

export interface TechStackCreate {
  name: string
  icon_url?: string | null
  display_order?: number
}

export interface TechStackUpdate {
  name?: string
  icon_url?: string | null
  display_order?: number
}
