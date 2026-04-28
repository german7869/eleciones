<template>
  <div class="max-w-sm mx-auto mt-16 p-6 bg-white rounded shadow">
    <h2 class="text-xl font-bold mb-4">Login Delegado</h2>
    <form @submit.prevent="login">
      <input v-model="cedula" type="text" placeholder="Cédula" class="input mb-2 w-full" />
      <input v-model="password" type="password" placeholder="Contraseña" class="input mb-4 w-full" />
      <button type="submit" class="btn w-full bg-blue-600 text-white">Entrar</button>
    </form>
    <div v-if="error" class="text-red-600 mt-2">{{ error }}</div>
  </div>
</template>
<script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const cedula = ref('');
const password = ref('');
const error = ref('');
const router = useRouter();

function getRol(token: string): string {
  try {
    return JSON.parse(atob(token.split('.')[1])).rol || '';
  } catch { return ''; }
}

async function login() {
  error.value = '';
  try {
    const res = await axios.post('/auth/login', { cedula: cedula.value, password: password.value });
    localStorage.setItem('token', res.data.access_token);
    axios.defaults.headers.common['Authorization'] = `Bearer ${res.data.access_token}`;
    
    // Redirigir según rol
    const rol = getRol(res.data.access_token);
    if (rol === 'admin') {
      router.push('/');
    } else if (rol === 'delegado') {
      router.push('/ingreso-votos');
    } else {
      router.push('/');
    }
  } catch (e: any) {
    error.value = e.response?.data?.detail || 'Error de autenticación';
  }
}
</script>
