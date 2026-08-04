/**
 * Composable for fetching projects from the backend API.
 * All data-fetching goes through composables — never inline in .vue files.
 */
import type { Project } from '~/types/project'

export function useProjects() {
  const config = useRuntimeConfig()
  const baseUrl = config.public.apiBaseUrl

  const { data: projects, status, refresh, error } = useFetch<Project[]>(
    `${baseUrl}/api/v1/projects`,
    {
      key: 'projects-list',
      default: () => [],
    },
  )

  return { projects, status, refresh, error }
}

export function useProject(slug: Ref<string> | string) {
  const config = useRuntimeConfig()
  const baseUrl = config.public.apiBaseUrl
  const slugValue = toRef(slug)

  const { data: project, status, refresh, error } = useFetch<Project>(
    () => `${baseUrl}/api/v1/projects/${slugValue.value}`,
    {
      key: `project-${slugValue.value}`,
    },
  )

  return { project, status, refresh, error }
}
