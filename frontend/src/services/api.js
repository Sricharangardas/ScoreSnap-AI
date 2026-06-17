import axios from 'axios';

// Detect API base URL, fallback to local FastAPI server
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Automatically attach JWT authorization token if it exists in local storage
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export const authAPI = {
  register: (name, email, password) => 
    api.post('/auth/register', { name, email, password }),
  
  login: (email, password) => 
    api.post('/auth/login', { email, password }),
  
  me: () => 
    api.get('/auth/me'),
};

export const matchesAPI = {
  getMatches: (status = null, group = null) => {
    const params = {};
    if (status) params.status = status;
    if (group) params.group = group;
    return api.get('/matches/', { params });
  },
  
  getMatchDetail: (matchId) => 
    api.get(`/matches/${matchId}`),
  
  getMatchAnalysis: (matchId, lang = 'English') => 
    api.get(`/matches/${matchId}/analysis`, { params: { lang } }),
  
  getMatchPrediction: (matchId) => 
    api.get(`/matches/${matchId}/prediction`),

  simulateKickoff: (matchId) => 
    api.post(`/matches/${matchId}/simulate-kickoff`),
  
  simulateFullTime: (matchId, score1, score2) => 
    api.post(`/matches/${matchId}/simulate-fulltime`, { score_1: score1, score_2: score2 }),
};

export const standingsAPI = {
  getStandings: () => 
    api.get('/standings/'),
  
  recalculateStandings: () => 
    api.post('/standings/recalculate'),
};

export const usersAPI = {
  updatePreferences: (preferences) => 
    api.put('/users/preferences', preferences),
};

export const cronAPI = {
  triggerMonitor: () => 
    api.get('/cron/monitor'),
  
  triggerDigest: () => 
    api.get('/cron/digest'),
};

export default api;
