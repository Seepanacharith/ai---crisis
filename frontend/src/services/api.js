import axios from 'axios';

const API_BASE = '/api/v1';

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Intercept requests to attach JWT token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  getMe: () => api.get('/auth/me'),
};

export const chatAPI = {
  sendQuery: (data) => api.post('/chat', data),
  getHistory: () => api.get('/chat/history'),
  clearHistory: () => api.delete('/chat/history'),
};

export const disasterAPI = {
  getAll: () => api.get('/disasters'),
  getByType: (type) => api.get(`/disasters/${type}`),
};

export const checklistAPI = {
  get: (disasterType) => api.get(`/checklists/${disasterType}`),
  save: (disasterType, items) => api.post('/checklists', { disaster_type: disasterType, items }),
};

export const alertAPI = {
  getAll: (disasterType = 'all') => api.get(`/alerts?disaster_type=${disasterType}`),
  getById: (id) => api.get(`/alerts/${id}`),
};

export const emergencyAPI = {
  getFacilities: (type = 'all', lat = 17.3850, lon = 78.4867) => api.get(`/emergency-services?type=${type}&lat=${lat}&lon=${lon}`),
  getShelters: () => api.get('/shelters'),
  getHospitals: () => api.get('/hospitals'),
};

export const metricsAPI = {
  getMetrics: () => api.get('/metrics'),
  getHealth: () => api.get('/health'),
};

export const adminAPI = {
  getStats: () => api.get('/admin/stats'),
};

export default api;
