import type { StatItem, StatCreate, StatUpdate } from '~/types/stat'

export function useAdminStats() {
  const config = useRuntimeConfig()
  const baseUrl = config.public.apiBaseUrl
  const { getAuthHeader } = useAuth()

  const { data: stats, status, refresh, error } = useFetch<StatItem[]>(
    `${baseUrl}/api/v1/stats`,
    {
      key: 'admin-stats-list',
      default: () => [],
      headers: computed(() => getAuthHeader()),
    },
  )

  /** Create a new stat card. */
  async function createStat(data: StatCreate): Promise<StatItem> {
    return await $fetch<StatItem>(`${baseUrl}/api/v1/stats`, {
      method: 'POST',
      body: data,
      headers: getAuthHeader(),
    })
  }

  /** Update an existing stat card. */
  async function updateStat(id: string, data: StatUpdate): Promise<StatItem> {
    return await $fetch<StatItem>(`${baseUrl}/api/v1/stats/${id}`, {
      method: 'PUT',
      body: data,
      headers: getAuthHeader(),
    })
  }

  /** Delete a stat card. */
  async function deleteStat(id: string): Promise<void> {
    await $fetch(`${baseUrl}/api/v1/stats/${id}`, {
      method: 'DELETE',
      headers: getAuthHeader(),
    })
  }

  /** Reorder stat cards by updating display_order. */
  async function updateOrder(id: string, newOrder: number): Promise<StatItem> {
    return await updateStat(id, { display_order: newOrder })
  }

  return {
    stats,
    status,
    refresh,
    error,
    createStat,
    updateStat,
    deleteStat,
    updateOrder,
  }
}
