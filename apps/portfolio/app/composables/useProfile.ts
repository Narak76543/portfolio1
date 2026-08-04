export function useProfile() {
  const config = useRuntimeConfig()
  const baseUrl = config.public.apiBaseUrl

  const { data: profile, status, refresh } = useFetch(`${baseUrl}/api/v1/profile`, {
    key: 'public-profile',
  })

  return {
    profile,
    status,
    refresh,
  }
}
