import axios from 'axios'

const API_BASE = import.meta.env.DEV ? 'http://localhost:8000/api' : '/api'

const api = axios.create({
  baseURL: API_BASE,
  timeout: 300000  // 5 分钟超时
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    const message = error.response?.data?.detail || error.message || '请求失败'
    return Promise.reject(new Error(message))
  }
)

/**
 * 上传文件
 */
export const uploadFile = async (file) => {
  const formData = new FormData()
  formData.append('file', file)

  return await api.post('/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}

/**
 * 开始处理任务
 */
export const startProcess = async (params) => {
  return await api.post('/process', null, { params })
}

/**
 * 获取任务状态
 */
export const getTaskStatus = async (taskId) => {
  return await api.get(`/task/${taskId}`)
}

/**
 * 下载结果文件
 */
export const downloadFile = (taskId) => {
  const url = `${API_BASE}/download/${taskId}`
  window.open(url, '_blank')
}

/**
 * 获取配置
 */
export const getConfig = async () => {
  return await api.get('/config')
}

/**
 * 更新配置
 */
export const updateConfig = async (params) => {
  return await api.post('/config', null, { params })
}

/**
 * 获取所有任务
 */
export const getAllTasks = async () => {
  return await api.get('/tasks')
}
