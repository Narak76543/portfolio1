/**
 * Admin projects composable — CRUD operations through the backend API.
 * All data-fetching goes through composables — never inline in .vue files.
 */
import type { Project, ProjectCreate, ProjectUpdate } from '~/types/project'

export function useAdminProjects() {
  const config = useRuntimeConfig()
  const baseUrl = config.public.apiBaseUrl
  const { getAuthHeader } = useAuth()

  /** List all projects. */
  const { data: projects, status, refresh, error } = useFetch<Project[]>(
    `${baseUrl}/api/v1/projects`,
    {
      key: 'admin-projects-list',
      default: () => [],
      headers: computed(() => getAuthHeader()),
    },
  )

  /** Create a new project. */
  async function createProject(data: ProjectCreate): Promise<Project> {
    return await $fetch<Project>(`${baseUrl}/api/v1/projects`, {
      method: 'POST',
      body: data,
      headers: getAuthHeader(),
    })
  }

  /** Update an existing project. */
  async function updateProject(id: string, data: ProjectUpdate): Promise<Project> {
    return await $fetch<Project>(`${baseUrl}/api/v1/projects/${id}`, {
      method: 'PUT',
      body: data,
      headers: getAuthHeader(),
    })
  }

  /** Delete a project. */
  async function deleteProject(id: string): Promise<void> {
    await $fetch(`${baseUrl}/api/v1/projects/${id}`, {
      method: 'DELETE',
      headers: getAuthHeader(),
    })
  }

  /** Upload a cover image and return the URL. */
  async function uploadImage(file: File): Promise<string> {
    const formData = new FormData()
    formData.append('file', file)

    const response = await $fetch<{ url: string }>(`${baseUrl}/api/v1/projects/upload-image`, {
      method: 'POST',
      body: formData,
      headers: getAuthHeader(),
    })
    return response.url
  }

  /** Get a single project by ID. */
  async function getProject(id: string): Promise<Project> {
    return await $fetch<Project>(`${baseUrl}/api/v1/projects/${id}`, {
      headers: getAuthHeader(),
    })
  }

  /** Update display order of a project. */
  async function updateOrder(id: string, newOrder: number): Promise<Project> {
    return await updateProject(id, { display_order: newOrder })
  }

  return {
    projects,
    status,
    refresh,
    error,
    createProject,
    updateProject,
    deleteProject,
    uploadImage,
    getProject,
    updateOrder,
  }
}
