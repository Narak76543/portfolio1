import type { SocialMediaItem } from '~/types/socialMedia'

export function useSocialMedia() {
  const config = useRuntimeConfig()
  const baseUrl = config.public.apiBaseUrl

  const { data: socialMedias, status, error } = useFetch<SocialMediaItem[]>(
    `${baseUrl}/api/v1/social-media`,
    {
      key: 'public-social-media-list',
      default: () => [],
    },
  )

  return {
    socialMedias,
    status,
    error,
  }
}
