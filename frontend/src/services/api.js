import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const getModules = async () => {
  try {
    const response = await api.get('/api/modules')
    return response.data.modules
  } catch (error) {
    console.error('Error fetching modules:', error)
    throw error
  }
}

export const buildApp = async (prompt) => {
  try {
    const response = await api.post('/api/build', { prompt })
    return response.data
  } catch (error) {
    console.error('Error building app:', error)
    throw error
  }
}

export const getFileContent = async (sessionId, filePath) => {
  try {
    const response = await api.get(`/api/file/${sessionId}/${filePath}`)
    return response.data.content
  } catch (error) {
    console.error('Error fetching file content:', error)
    throw error
  }
}

export default api
