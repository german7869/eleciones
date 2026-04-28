<template>
  <div class="min-h-screen bg-gray-50 p-6">
    <div class="max-w-7xl mx-auto">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-800 mb-2">Juntas Asignadas - Progreso</h1>
        <p class="text-gray-600">Monitorea el estado de ingreso de votos por delegado</p>
      </div>

      <!-- Stats -->
      <div class="grid grid-cols-4 gap-4 mb-8">
        <div class="bg-blue-50 p-4 rounded-lg border border-blue-200">
          <p class="text-sm text-blue-600 font-semibold">Total Juntas</p>
          <p class="text-3xl font-bold text-blue-800">{{ totalJuntas }}</p>
        </div>
        <div class="bg-green-50 p-4 rounded-lg border border-green-200">
          <p class="text-sm text-green-600 font-semibold">Procesadas</p>
          <p class="text-3xl font-bold text-green-800">{{ juntasProcesadas }}</p>
        </div>
        <div class="bg-yellow-50 p-4 rounded-lg border border-yellow-200">
          <p class="text-sm text-yellow-600 font-semibold">Pendientes</p>
          <p class="text-3xl font-bold text-yellow-800">{{ juntasPendientes }}</p>
        </div>
        <div class="bg-purple-50 p-4 rounded-lg border border-purple-200">
          <p class="text-sm text-purple-600 font-semibold">Progreso</p>
          <p class="text-3xl font-bold text-purple-800">{{ progresoPorc }}%</p>
        </div>
      </div>

      <!-- Filters -->
      <div class="bg-white rounded-lg shadow-md p-6 mb-6">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <!-- Filtro Estado -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">Estado</label>
            <select
              v-model="filtroEstado"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Todos</option>
              <option value="procesada">Procesadas</option>
              <option value="pendiente">Pendientes</option>
            </select>
          </div>

          <!-- Filtro Territorio (Parroquia) -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">Parroquia</label>
            <select
              v-model="filtroParroquia"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Todas</option>
              <option v-for="p in parroquias" :key="p.id" :value="p.id">
                {{ p.nombre }}
              </option>
            </select>
          </div>

          <!-- Búsqueda -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">Buscar</label>
            <input
              v-model="filtroSearch"
              type="text"
              placeholder="Junta, recinto, delegado..."
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="text-center py-12">
        <p class="text-gray-600">Cargando datos...</p>
      </div>

      <!-- Tabla de Juntas -->
      <div v-else class="bg-white rounded-lg shadow-md overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-gray-100 border-b border-gray-300">
              <tr>
                <th class="text-left px-4 py-3 font-semibold text-gray-700">Junta</th>
                <th class="text-left px-4 py-3 font-semibold text-gray-700">Recinto</th>
                <th class="text-left px-4 py-3 font-semibold text-gray-700">Parroquia</th>
                <th class="text-left px-4 py-3 font-semibold text-gray-700">Delegado</th>
                <th class="text-center px-4 py-3 font-semibold text-gray-700">Estado</th>
                <th class="text-center px-4 py-3 font-semibold text-gray-700">Votos</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="junta in juntasFiltradas" :key="junta.id" class="border-b border-gray-200 hover:bg-gray-50">
                <td class="px-4 py-3 text-gray-800 font-semibold">{{ junta.nombre }}</td>
                <td class="px-4 py-3 text-gray-600">{{ junta.recinto_nombre }}</td>
                <td class="px-4 py-3 text-gray-600">{{ junta.parroquia_nombre }}</td>
                <td class="px-4 py-3 text-gray-600">{{ junta.delegado_nombre || 'Sin asignar' }}</td>
                <td class="px-4 py-3 text-center">
                  <span
                    :class="[
                      'px-3 py-1 rounded-full text-sm font-semibold',
                      junta.estado === 'procesada'
                        ? 'bg-green-100 text-green-800'
                        : 'bg-yellow-100 text-yellow-800'
                    ]"
                  >
                    {{ junta.estado === 'procesada' ? '✓ Procesada' : '⏳ Pendiente' }}
                  </span>
                </td>
                <td class="px-4 py-3 text-center text-gray-600">{{ junta.total_votos || 0 }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Empty State -->
        <div v-if="juntasFiltradas.length === 0" class="text-center py-12">
          <p class="text-gray-500">No hay juntas que coincidan con los filtros</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

interface Junta {
  id: number
  nombre: string
  codigo: string
  tipo: string
  nro_votantes: number
  estado: string
  delegado_id?: number
  delegado_nombre?: string
  recinto_id: number
  recinto_nombre: string
  parroquia_nombre: string
  parroquia_id: number
  total_votos?: number
}

interface Parroquia {
  id: number
  nombre: string
}

const juntas = ref<Junta[]>([])
const parroquias = ref<Parroquia[]>([])
const loading = ref(true)
const filtroEstado = ref('')
const filtroParroquia = ref('')
const filtroSearch = ref('')

const totalJuntas = computed(() => juntas.value.length)
const juntasProcesadas = computed(() => juntas.value.filter(j => j.estado === 'procesada').length)
const juntasPendientes = computed(() => juntas.value.filter(j => j.estado === 'pendiente').length)
const progresoPorc = computed(() => {
  if (totalJuntas.value === 0) return 0
  return Math.round((juntasProcesadas.value / totalJuntas.value) * 100)
})

const juntasFiltradas = computed(() => {
  let filtered = juntas.value

  if (filtroEstado.value) {
    filtered = filtered.filter(j => j.estado === filtroEstado.value)
  }

  if (filtroParroquia.value) {
    filtered = filtered.filter(j => j.parroquia_id === parseInt(filtroParroquia.value))
  }

  if (filtroSearch.value) {
    const q = filtroSearch.value.toLowerCase()
    filtered = filtered.filter(j =>
      j.nombre.toLowerCase().includes(q) ||
      j.recinto_nombre.toLowerCase().includes(q) ||
      (j.delegado_nombre?.toLowerCase().includes(q) || false)
    )
  }

  return filtered
})

const cargar_datos = async () => {
  try {
    loading.value = true

    // Cargar parroquias
    const parroquiasRes = await axios.get('/api/parroquias/')
    parroquias.value = parroquiasRes.data

    // Cargar juntas
    const juntasRes = await axios.get('/api/juntas/')
    
    // Enriquecer juntas con información de delegados y votos
    const juntasEnriquecidas = await Promise.all(
      juntasRes.data.map(async (junta: any) => {
        let delegado_nombre = 'Sin asignar'
        let total_votos = 0
        let parroquia_nombre = ''

        if (junta.delegado_id) {
          try {
            const delRes = await axios.get(`/api/delegados/${junta.delegado_id}`)
            delegado_nombre = delRes.data.nombre
          } catch {}
        }

        // Obtener votos
        try {
          const votosRes = await axios.get(`/api/votos/junta/${junta.id}`)
          total_votos = votosRes.data.length
        } catch {}

        // Obtener parroquia
        if (junta.recinto_id) {
          try {
            const recintoRes = await axios.get(`/api/recintos/${junta.recinto_id}`)
            const recinto = recintoRes.data
            if (recinto.zona_id) {
              const zonaRes = await axios.get(`/api/zonas/${recinto.zona_id}`)
              const zona = zonaRes.data
              if (zona.parroquia_id) {
                const parRes = await axios.get(`/api/parroquias/${zona.parroquia_id}`)
                parroquia_nombre = parRes.data.nombre
              }
            }
          } catch {}
        }

        return {
          ...junta,
          delegado_nombre,
          total_votos,
          parroquia_nombre,
          parroquia_id: junta.parroquia_id || 0
        }
      })
    )

    juntas.value = juntasEnriquecidas
  } catch (err: any) {
    console.error('Error al cargar datos:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  cargar_datos()
})
</script>
