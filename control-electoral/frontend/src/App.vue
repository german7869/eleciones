<template>
  <nav class="bg-blue-600 text-white p-4 flex gap-4">
    <router-link to="/" class="hover:underline">Inicio</router-link>
    <router-link to="/resultados" class="hover:underline">Resultados</router-link>
    <router-link to="/reporte" class="hover:underline">Reporte de Votos</router-link>
    <router-link to="/acta" class="hover:underline">Subir Acta</router-link>
    <span class="flex-1"></span>
    <template v-if="isAuth">
      <button @click="logout" class="ml-2 bg-white text-blue-600 px-3 py-1 rounded">Cerrar sesión</button>
    </template>
    <router-link v-else to="/login" class="hover:underline ml-auto">Login</router-link>
  </nav>
  <router-view />
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const isAuth = computed(() => !!localStorage.getItem('token'));

function logout() {
  localStorage.removeItem('token');
  window.location.reload();
}
</script>
</script>

<style>
body { background: #f8fafc; }
</style>
