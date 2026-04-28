<template>
  <div class="p-8 max-w-6xl mx-auto">
    <!-- PANEL ADMIN -->
    <template v-if="isAdmin">
      <h1 class="text-3xl font-bold mb-8">Panel de Administrador</h1>
      
      <!-- Estadísticas Dashboard para Admin (Primero) -->
      <div v-if="!loading" class="mb-12">
        <h2 class="text-2xl font-bold mb-4">Resumen del Sistema</h2>
        <div class="grid grid-cols-2 md:grid-cols-3 gap-4">
          <div class="bg-blue-50 rounded shadow p-4">
            <p class="text-sm text-gray-600">Total Juntas</p>
            <p class="text-3xl font-bold text-blue-600">{{ stats.juntas_total }}</p>
          </div>
          <div class="bg-green-50 rounded shadow p-4">
            <p class="text-sm text-gray-600">Juntas Reportadas</p>
            <p class="text-3xl font-bold text-green-600">{{ stats.juntas_reportadas }}</p>
          </div>
          <div class="bg-purple-50 rounded shadow p-4">
            <p class="text-sm text-gray-600">Actas Subidas</p>
            <p class="text-3xl font-bold text-purple-600">{{ stats.actas_subidas }}</p>
          </div>
          <div class="bg-gray-50 rounded shadow p-4">
            <p class="text-sm text-gray-600">Total Votos</p>
            <p class="text-3xl font-bold text-gray-800">{{ stats.total_votos }}</p>
          </div>
          <div class="bg-red-50 rounded shadow p-4">
            <p class="text-sm text-gray-600">Votos Nulos</p>
            <p class="text-3xl font-bold text-red-500">{{ stats.total_nulos }}</p>
          </div>
          <div class="bg-yellow-50 rounded shadow p-4">
            <p class="text-sm text-gray-600">Votos en Blanco</p>
            <p class="text-3xl font-bold text-yellow-500">{{ stats.total_blancos }}</p>
          </div>
        </div>
      </div>
      
      <!-- Opciones (Después) -->
      <div>
        <h2 class="text-2xl font-bold mb-4">Opciones</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <!-- Gestión de Delegados -->
        <router-link to="/admin/delegados" class="bg-white rounded shadow hover:shadow-lg transition p-6 cursor-pointer">
          <div class="text-4xl mb-2">👤</div>
          <h3 class="text-lg font-bold mb-2">Gestión de Delegados</h3>
          <p class="text-gray-600 text-sm mb-4">Crear, editar y administrar delegados</p>
          <div class="text-blue-600 text-sm font-semibold">Ir →</div>
        </router-link>

        <!-- Cambiar Claves de Delegados -->
        <router-link to="/admin/cambiar-claves" class="bg-white rounded shadow hover:shadow-lg transition p-6 cursor-pointer">
          <div class="text-4xl mb-2">🔐</div>
          <h3 class="text-lg font-bold mb-2">Cambiar Claves</h3>
          <p class="text-gray-600 text-sm mb-4">Cambiar contraseñas de delegados</p>
          <div class="text-blue-600 text-sm font-semibold">Ir →</div>
        </router-link>

        <!-- Asignar Juntas a Delegados -->
        <router-link to="/admin/asignar-juntas" class="bg-white rounded shadow hover:shadow-lg transition p-6 cursor-pointer">
          <div class="text-4xl mb-2">🎯</div>
          <h3 class="text-lg font-bold mb-2">Asignar Juntas</h3>
          <p class="text-gray-600 text-sm mb-4">Asignar juntas a delegados para ingreso de votos</p>
          <div class="text-blue-600 text-sm font-semibold">Ir →</div>
        </router-link>

        <!-- Resumen de Juntas -->
        <router-link to="/admin/resumen-juntas" class="bg-white rounded shadow hover:shadow-lg transition p-6 cursor-pointer">
          <div class="text-4xl mb-2">📊</div>
          <h3 class="text-lg font-bold mb-2">Resumen de Juntas</h3>
          <p class="text-gray-600 text-sm mb-4">Ver progreso de procesamiento por delegado</p>
          <div class="text-blue-600 text-sm font-semibold">Ir →</div>
        </router-link>

        <!-- Asignar Delegados a Juntas -->
        <router-link to="/admin/asignar-delegados" class="bg-white rounded shadow hover:shadow-lg transition p-6 cursor-pointer">
          <div class="text-4xl mb-2">🔗</div>
          <h3 class="text-lg font-bold mb-2">Asignar Delegados</h3>
          <p class="text-gray-600 text-sm mb-4">Asignar delegados a juntas electorales</p>
          <div class="text-blue-600 text-sm font-semibold">Ir →</div>
        </router-link>

        <!-- Gestión de Partidos -->
        <router-link to="/admin/partidos" class="bg-white rounded shadow hover:shadow-lg transition p-6 cursor-pointer">
          <div class="text-4xl mb-2">🏛️</div>
          <h3 class="text-lg font-bold mb-2">Gestión de Partidos</h3>
          <p class="text-gray-600 text-sm mb-4">Crear y administrar partidos políticos</p>
          <div class="text-blue-600 text-sm font-semibold">Ir →</div>
        </router-link>

        <!-- Gestión de Territorios -->
        <router-link to="/admin/territorios" class="bg-white rounded shadow hover:shadow-lg transition p-6 cursor-pointer">
          <div class="text-4xl mb-2">🗺️</div>
          <h3 class="text-lg font-bold mb-2">Gestión de Territorios</h3>
          <p class="text-gray-600 text-sm mb-4">Administrar parroquias, zonas, recintos y juntas</p>
          <div class="text-blue-600 text-sm font-semibold">Ir →</div>
        </router-link>

        <!-- Subir Acta -->
        <router-link to="/acta" class="bg-white rounded shadow hover:shadow-lg transition p-6 cursor-pointer">
          <div class="text-4xl mb-2">📄</div>
          <h3 class="text-lg font-bold mb-2">Subir Acta</h3>
          <p class="text-gray-600 text-sm mb-4">Procesar actas electorales</p>
          <div class="text-blue-600 text-sm font-semibold">Ir →</div>
        </router-link>

        <!-- Reporte de Votos -->
        <router-link to="/reporte" class="bg-white rounded shadow hover:shadow-lg transition p-6 cursor-pointer">
          <div class="text-4xl mb-2">📊</div>
          <h3 class="text-lg font-bold mb-2">Reporte de Votos</h3>
          <p class="text-gray-600 text-sm mb-4">Registrar y consultar votos por junta</p>
          <div class="text-blue-600 text-sm font-semibold">Ir →</div>
        </router-link>

        <!-- Resultados -->
        <router-link to="/resultados" class="bg-white rounded shadow hover:shadow-lg transition p-6 cursor-pointer">
          <div class="text-4xl mb-2">📈</div>
          <h3 class="text-lg font-bold mb-2">Resultados Electorales</h3>
          <p class="text-gray-600 text-sm mb-4">Ver resultados consolidados</p>
          <div class="text-blue-600 text-sm font-semibold">Ir →</div>
        </router-link>
      </div>
      </div>
    </template>

    <!-- PANEL DELEGADO -->
    <template v-else>
      <h1 class="text-2xl font-bold mb-6">Panel del Delegado Electoral</h1>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Ingreso de Votos (Página Principal) -->
        <router-link to="/ingreso-votos" class="bg-white rounded shadow hover:shadow-lg transition p-6 cursor-pointer border-l-4 border-green-600">
          <div class="text-4xl mb-2">✍️</div>
          <h3 class="text-lg font-bold mb-2">Ingreso de Votos</h3>
          <p class="text-gray-600 text-sm mb-4">Registrar votos para tu junta asignada</p>
          <div class="text-green-600 text-sm font-semibold">Ir →</div>
        </router-link>

        <!-- Resultados -->
        <router-link to="/resultados" class="bg-white rounded shadow hover:shadow-lg transition p-6 cursor-pointer">
          <div class="text-4xl mb-2">📈</div>
          <h3 class="text-lg font-bold mb-2">Resultados Electorales</h3>
          <p class="text-gray-600 text-sm mb-4">Ver resultados consolidados de las elecciones</p>
          <div class="text-blue-600 text-sm font-semibold">Ir →</div>
        </router-link>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

const loading = ref(true)
const stats = ref({
  juntas_total: 0,
  juntas_reportadas: 0,
  actas_subidas: 0,
  total_votos: 0,
  total_nulos: 0,
  total_blancos: 0,
  progreso_pct: 0,
})

function getRol(): string {
  const token = localStorage.getItem('token')
  if (!token) return ''
  try {
    return JSON.parse(atob(token.split('.')[1])).rol || ''
  } catch {
    return ''
  }
}

const isAdmin = computed(() => getRol() === 'admin')

onMounted(async () => {
  try {
    const res = await axios.get('http://localhost:8000/dashboard/')
    stats.value = res.data
  } catch {
    // sin datos aún
  }
  loading.value = false
})
</script>
