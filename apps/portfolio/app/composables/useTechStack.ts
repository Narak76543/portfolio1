import type { TechStackItem } from '~/types/techStack'

export function useTechStack() {
  const config = useRuntimeConfig()
  const baseUrl = config.public.apiBaseUrl

  const { data: techStacks, status, error } = useFetch<TechStackItem[]>(
    `${baseUrl}/api/v1/tech-stack`,
    {
      key: 'public-tech-stack-list',
      default: () => [],
    },
  )

  return {
    techStacks,
    status,
    error,
  }
}
