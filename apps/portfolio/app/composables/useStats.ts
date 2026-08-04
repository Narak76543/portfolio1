import type { StatItem } from '~/types/stat'

export function useStats() {
  const config = useRuntimeConfig()
  const baseUrl = config.public.apiBaseUrl

  const { data: stats, status, error } = useFetch<StatItem[]>(
    `${baseUrl}/api/v1/stats`,
    {
      key: 'public-stats-list',
      default: () => [],
    },
  )

  return {
    stats,
    status,
    error,
  }
}
