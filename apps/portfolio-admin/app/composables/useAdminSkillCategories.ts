import type { SkillCategory } from '~/types/skillCategory'

export function useAdminSkillCategories() {
  const config = useRuntimeConfig()
  const baseUrl = config.public.apiBaseUrl
  const { getAuthHeader } = useAuth()

  const { data: categories, status, refresh } = useFetch<SkillCategory[]>(
    `${baseUrl}/api/v1/skill-categories`,
    {
      headers: computed(() => getAuthHeader()),
      key: 'admin-skill-categories',
    }
  )

  async function createCategory(data: { name: string; icon_name: string; items: string[]; display_order?: number }) {
    return await $fetch<SkillCategory>(`${baseUrl}/api/v1/skill-categories`, {
      method: 'POST',
      headers: getAuthHeader(),
      body: data,
    })
  }

  async function updateCategory(id: string, data: { name?: string; icon_name?: string; items?: string[]; display_order?: number }) {
    return await $fetch<SkillCategory>(`${baseUrl}/api/v1/skill-categories/${id}`, {
      method: 'PUT',
      headers: getAuthHeader(),
      body: data,
    })
  }

  async function deleteCategory(id: string) {
    return await $fetch(`${baseUrl}/api/v1/skill-categories/${id}`, {
      method: 'DELETE',
      headers: getAuthHeader(),
    })
  }

  return {
    categories,
    status,
    refresh,
    createCategory,
    updateCategory,
    deleteCategory,
  }
}
