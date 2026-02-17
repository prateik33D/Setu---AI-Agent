import { useAuth } from '@clerk/clerk-react'
import { useState, useCallback } from 'react'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const useSetuAPI = () => {
  const { getToken, isSignedIn } = useAuth()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const makeRequest = useCallback(async (endpoint, options = {}) => {
    if (!isSignedIn) {
      throw new Error('User must be signed in')
    }

    setLoading(true)
    setError(null)

    try {
      const token = await getToken()

      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
          ...options.headers,
        },
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        const message = typeof errorData.detail === 'string'
          ? errorData.detail
          : Array.isArray(errorData.detail)
            ? errorData.detail.map((x) => x?.msg || String(x)).join(', ')
            : `Request failed: ${response.status}`
        throw new Error(message)
      }

      return await response.json()
    } catch (err) {
      setError(err.message)
      throw err
    } finally {
      setLoading(false)
    }
  }, [getToken, isSignedIn])

  const createTask = useCallback(async (description, priority = 'medium') => {
    return makeRequest('/api/v1/tasks/create', {
      method: 'POST',
      body: JSON.stringify({ description, priority }),
    })
  }, [makeRequest])

  const getTask = useCallback(async (taskId) => {
    return makeRequest(`/api/v1/tasks/${taskId}`)
  }, [makeRequest])

  const listTasks = useCallback(async (status = null) => {
    const params = status ? `?status=${status}` : ''
    return makeRequest(`/api/v1/tasks${params}`)
  }, [makeRequest])

  const deleteTask = useCallback(async (taskId) => {
    return makeRequest(`/api/v1/tasks/${taskId}`, { method: 'DELETE' })
  }, [makeRequest])

  const initiateGoogleAuth = useCallback(async () => {
    const data = await makeRequest('/api/v1/auth/google/login')
    if (data.auth_url) window.location.href = data.auth_url
    return data
  }, [makeRequest])

  const initiateNotionAuth = useCallback(async () => {
    const data = await makeRequest('/api/v1/auth/notion/login')
    if (data.auth_url) window.location.href = data.auth_url
    return data
  }, [makeRequest])

  const initiateSlackAuth = useCallback(async () => {
    const data = await makeRequest('/api/v1/auth/slack/login')
    if (data.auth_url) window.location.href = data.auth_url
    return data
  }, [makeRequest])

  const initiateGitHubAuth = useCallback(async () => {
    const data = await makeRequest('/api/v1/auth/github/login')
    if (data.auth_url) window.location.href = data.auth_url
    return data
  }, [makeRequest])

  const listIntegrations = useCallback(async () => {
    return makeRequest('/api/v1/integrations')
  }, [makeRequest])

  const disconnectIntegration = useCallback(async (integrationId) => {
    return makeRequest(`/api/v1/integrations/${integrationId}`, { method: 'DELETE' })
  }, [makeRequest])

  const healthCheck = useCallback(async () => {
    const response = await fetch(`${API_BASE_URL}/health`)
    return response.json()
  }, [])

  return {
    loading,
    error,
    createTask,
    getTask,
    listTasks,
    deleteTask,
    initiateGoogleAuth,
    initiateNotionAuth,
    initiateSlackAuth,
    initiateGitHubAuth,
    listIntegrations,
    disconnectIntegration,
    healthCheck,
  }
}
