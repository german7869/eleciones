<template>
  <nav class="bg-blue-600 text-white p-4 flex gap-4 flex-wrap items-center">
    <router-link to="/" class="hover:underline font-semibold">Inicio</router-link>
    <router-link to="/resultados" class="hover:underline">Resultados</router-link>
    <template v-if="isAuth">
      <router-link to="/reporte" class="hover:underline">Reporte de Votos</router-link>
      <router-link to="/acta" class="hover:underline">Subir Acta</router-link>
    </template>
    <template v-if="isAdmin">
      <span class="text-blue-300">|</span>
      <router-link to="/admin/delegados" class="hover:underline text-blue-200">Delegados</router-link>
      <router-link to="/admin/partidos" class="hover:underline text-blue-200">Partidos</router-link>
      <router-link to="/admin/territorios" class="hover:underline text-blue-200">Territorios</router-link>
    </template>
    <span class="flex-1"></span>
    <template v-if="isAuth">
      <span class="text-blue-200 text-sm">{{ rolLabel }}</span>
      <button @click="logout" class="ml-2 bg-white text-blue-600 px-3 py-1 rounded text-sm">Cerrar sesión</button>
    </template>
    <router-link v-else to="/login" class="hover:underline ml-auto">Login</router-link>
  </nav>
  <router-view />
  <Toast />
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import Toast from './components/Toast.vue';

const router = useRouter();

function getRol(): string {
  const token = localStorage.getItem('token');
  if (!token) return '';
  try {
    return JSON.parse(atob(token.split('.')[1])).rol || '';
  } catch { return ''; }
}

const isAuth = computed(() => !!localStorage.getItem('token'));
const isAdmin = computed(() => getRol() === 'admin');
const rolLabel = computed(() => getRol() === 'admin' ? 'Admin' : 'Delegado');

function logout() {
  localStorage.removeItem('token');
  router.push({ name: 'Login' });
}
</script>

<style>
body { background: #f8fafc; }
.input { border: 1px solid #d1d5db; border-radius: 0.375rem; padding: 0.375rem 0.75rem; font-size: 0.875rem; outline: none; }
.input:focus { border-color: #2563eb; box-shadow: 0 0 0 2px rgba(37,99,235,0.2); }
.btn { cursor: pointer; border-radius: 0.375rem; padding: 0.375rem 0.75rem; font-size: 0.875rem; }
</style>
