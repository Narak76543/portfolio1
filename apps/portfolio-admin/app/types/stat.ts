export interface StatItem {
  id: string
  label: string
  value: string
  icon_name?: string | null
  display_order: number
  created_at?: string
}

export interface StatCreate {
  label: string
  value: string
  icon_name?: string | null
  display_order?: number
}

export interface StatUpdate {
  label?: string
  value?: string
  icon_name?: string | null
  display_order?: number
}
