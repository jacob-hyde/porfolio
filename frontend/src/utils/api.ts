import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8092';

interface Project {
  id: number;
  title: string;
  description: string;
  image_url?: string;
  github_url?: string;
  live_url?: string;
  tech_stack?: string[];
  created_at?: string;
}

interface Skill {
  id: number;
  name: string;
  category: string;
  proficiency: number;
  created_at?: string;
}

interface LoginRequest {
  username: string;
  password: string;
}

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
    }
    return Promise.reject(error);
  }
);

export const authApi = {
  login: async (username: string, password: string) => {
    const response = await api.post('/login', { username, password });
    if (response.data.token) {
      localStorage.setItem('token', response.data.token);
    }
    return response.data;
  },
  checkAuth: async () => api.get('/check-auth'),
  logout: () => {
    localStorage.removeItem('token');
  },
};

export const projectsApi = {
  list: () => api.get('/projects'),
  create: (project: Omit<Project, 'id'>) => api.post('/projects', project),
  delete: (id: number) => api.delete(`/projects/${id}`),
};

export const skillsApi = {
  list: () => api.get('/skills'),
  create: (skill: Omit<Skill, 'id'>) => api.post('/skills', skill),
  delete: (id: number) => api.delete(`/skills/${id}`),
};

export const profileApi = {
  get: () => api.get('/profile'),
};

export default api;
