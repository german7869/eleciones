import { createApp } from 'vue';
import App from './App.vue';
import './index.css';
import router from './router';
import axios from 'axios';

// Base URL del backend
axios.defaults.baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Adjuntar token JWT en cada petición
axios.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Manejar 401: limpiar sesión y redirigir a login
axios.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('rol');
      router.push({ name: 'Login' });
    }
    return Promise.reject(error);
  }
);

const app = createApp(App);
app.use(router);
app.mount('#app');
