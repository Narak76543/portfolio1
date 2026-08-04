import type { TechStackItem, TechStackCreate, TechStackUpdate } from '~/types/techStack'

export function useAdminTechStack() {
  const config = useRuntimeConfig()
  const baseUrl = config.public.apiBaseUrl
  const { getAuthHeader } = useAuth()

  const { data: techStacks, status, refresh, error } = useFetch<TechStackItem[]>(
    `${baseUrl}/api/v1/tech-stack`,
    {
      key: 'admin-tech-stack-list',
      default: () => [],
      headers: computed(() => getAuthHeader()),
    },
  )

  /** Create a new tech stack item. */
  async function createTechStack(data: TechStackCreate): Promise<TechStackItem> {
    return await $fetch<TechStackItem>(`${baseUrl}/api/v1/tech-stack`, {
      method: 'POST',
      body: data,
      headers: getAuthHeader(),
    })
  }

  /** Update an existing tech stack item. */
  async function updateTechStack(id: string, data: TechStackUpdate): Promise<TechStackItem> {
    return await $fetch<TechStackItem>(`${baseUrl}/api/v1/tech-stack/${id}`, {
      method: 'PUT',
      body: data,
      headers: getAuthHeader(),
    })
  }

  /** Delete a tech stack item. */
  async function deleteTechStack(id: string): Promise<void> {
    await $fetch(`${baseUrl}/api/v1/tech-stack/${id}`, {
      method: 'DELETE',
      headers: getAuthHeader(),
    })
  }

  /** Upload an icon file and return the public URL. */
  async function uploadIcon(file: File): Promise<string> {
    const formData = new FormData()
    formData.append('file', file)

    const response = await $fetch<{ url: string }>(`${baseUrl}/api/v1/tech-stack/upload-icon`, {
      method: 'POST',
      body: formData,
      headers: getAuthHeader(),
    })
    return response.url
  }

  /** Reorder tech stack items by swapping or updating display_order. */
  async function updateOrder(id: string, newOrder: number): Promise<TechStackItem> {
    return await updateTechStack(id, { display_order: newOrder })
  }

  return {
    techStacks,
    status,
    refresh,
    error,
    createTechStack,
    updateTechStack,
    deleteTechStack,
    uploadIcon,
    updateOrder,
  }
}
