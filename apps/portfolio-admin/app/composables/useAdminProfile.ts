export function useAdminProfile() {
  const config = useRuntimeConfig()
  const baseUrl = config.public.apiBaseUrl
  const { authState, getAuthHeader } = useAuth()

  // Fetch the profile
  const { data: profile, status, refresh } = useFetch(`${baseUrl}/api/v1/profile`, {
    headers: computed(() => getAuthHeader()),
    key: 'admin-profile',
  })

  // Upload new avatar
  async function uploadAvatar(file: File) {
    const headers = getAuthHeader()
    if (!headers.Authorization) {
      throw new Error('Not authenticated')
    }

    const formData = new FormData()
    formData.append('file', file)

    return await $fetch(`${baseUrl}/api/v1/profile/upload-avatar`, {
      method: 'POST',
      headers,
      body: formData,
    })
  }

  // Upload new logo image
  async function uploadLogo(file: File) {
    const headers = getAuthHeader()
    if (!headers.Authorization) {
      throw new Error('Not authenticated')
    }

    const formData = new FormData()
    formData.append('file', file)

    return await $fetch(`${baseUrl}/api/v1/profile/upload-logo`, {
      method: 'POST',
      headers,
      body: formData,
    })
  }

  // Upload new heading font
  async function uploadFont(file: File, fontName?: string) {
    const headers = getAuthHeader()
    if (!headers.Authorization) {
      throw new Error('Not authenticated')
    }

    const formData = new FormData()
    formData.append('file', file)
    if (fontName) {
      formData.append('font_name', fontName)
    }

    const query = fontName ? `?font_name=${encodeURIComponent(fontName)}` : ''

    return await $fetch(`${baseUrl}/api/v1/profile/upload-font${query}`, {
      method: 'POST',
      headers,
      body: formData,
    })
  }

  // Update profile attributes (tagline, about, logo settings, heading font)
  async function updateProfile(data: {
    tagline?: string
    about_heading?: string
    about_subheading?: string
    about_bio?: string
    logo_type?: string
    logo_text?: string
    logo_image_url?: string | null
    heading_font_url?: string | null
    heading_font_name?: string | null
    first_name?: string
    last_name?: string
    hero_pitch?: string
  }) {
    const headers = getAuthHeader()
    if (!headers.Authorization) {
      throw new Error('Not authenticated')
    }

    return await $fetch(`${baseUrl}/api/v1/profile`, {
      method: 'PUT',
      headers,
      body: data,
    })
  }

  return {
    profile,
    status,
    refresh,
    uploadAvatar,
    uploadLogo,
    uploadFont,
    updateProfile,
  }
}
