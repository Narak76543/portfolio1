import type { SkillCategory } from '~/types/skillCategory'

export function useSkillCategories() {
  const config = useRuntimeConfig()
  const baseUrl = config.public.apiBaseUrl

  const { data: categories, status, refresh } = useFetch<SkillCategory[]>(
    `${baseUrl}/api/v1/skill-categories`,
    { key: 'public-skill-categories' }
  )

  return {
    categories,
    status,
    refresh,
  }
}
