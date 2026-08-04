import type { SocialMediaItem, SocialMediaCreate, SocialMediaUpdate } from '~/types/socialMedia'

export function useAdminSocialMedia() {
  const config = useRuntimeConfig()
  const baseUrl = config.public.apiBaseUrl
  const { getAuthHeader } = useAuth()

  const { data: socialMedias, status, refresh, error } = useFetch<SocialMediaItem[]>(
    `${baseUrl}/api/v1/social-media`,
    {
      key: 'admin-social-media-list',
      default: () => [],
      headers: computed(() => getAuthHeader()),
    },
  )

  /** Create a new social media link item. */
  async function createSocialMedia(data: SocialMediaCreate): Promise<SocialMediaItem> {
    return await $fetch<SocialMediaItem>(`${baseUrl}/api/v1/social-media`, {
      method: 'POST',
      body: data,
      headers: getAuthHeader(),
    })
  }

  /** Update an existing social media item. */
  async function updateSocialMedia(id: string, data: SocialMediaUpdate): Promise<SocialMediaItem> {
    return await $fetch<SocialMediaItem>(`${baseUrl}/api/v1/social-media/${id}`, {
      method: 'PUT',
      body: data,
      headers: getAuthHeader(),
    })
  }

  /** Delete a social media item. */
  async function deleteSocialMedia(id: string): Promise<void> {
    await $fetch(`${baseUrl}/api/v1/social-media/${id}`, {
      method: 'DELETE',
      headers: getAuthHeader(),
    })
  }

  /** Upload a social media icon file and return the public URL. */
  async function uploadIcon(file: File): Promise<string> {
    const formData = new FormData()
    formData.append('file', file)

    const response = await $fetch<{ url: string }>(`${baseUrl}/api/v1/social-media/upload-icon`, {
      method: 'POST',
      body: formData,
      headers: getAuthHeader(),
    })
    return response.url
  }

  /** Reorder social media items by updating display_order. */
  async function updateOrder(id: string, newOrder: number): Promise<SocialMediaItem> {
    return await updateSocialMedia(id, { display_order: newOrder })
  }

  return {
    socialMedias,
    status,
    refresh,
    error,
    createSocialMedia,
    updateSocialMedia,
    deleteSocialMedia,
    uploadIcon,
    updateOrder,
  }
}
