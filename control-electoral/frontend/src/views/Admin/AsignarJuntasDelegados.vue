<template>
  <div class="min-h-screen bg-gray-50 p-6">
    <div class="max-w-6xl mx-auto">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-800 mb-2">Asignar Juntas a Delegados</h1>
        <p class="text-gray-600">Selecciona un delegado y asigna 1 o más juntas para que ingrese votos</p>
      </div>

      <!-- Stats -->
      <div class="grid grid-cols-3 gap-4 mb-8">
        <div class="bg-blue-50 p-4 rounded-lg border border-blue-200">
          <p class="text-sm text-blue-600 font-semibold">Delegados</p>
          <p class="text-3xl font-bold text-blue-800">{{ delegados.length }}</p>
        </div>
        <div class="bg-green-50 p-4 rounded-lg border border-green-200">
          <p class="text-sm text-green-600 font-semibold">Juntas Disponibles</p>
          <p class="text-3xl font-bold text-green-800">{{ juntasDisponibles.length }}</p>
        </div>
        <div class="bg-purple-50 p-4 rounded-lg border border-purple-200">
          <p class="text-sm text-purple-600 font-semibold">Juntas Asignadas</p>
          <p class="text-3xl font-bold text-purple-800">{{ juntasAsignadas }}</p>
        </div>
      </div>

      <!-- Error/Success Messages -->
      <div v-if="error" class="bg-red-50 border border-red-200 text-red-800 px-4 py-3 rounded mb-4">
        {{ error }}
      </div>
      <div v-if="successMessage" class="bg-green-50 border border-green-200 text-green-800 px-4 py-3 rounded mb-4">
        {{ successMessage }}
      </div>

      <!-- Loading -->
      <div v-if="loading" class="text-center py-12">
        <p class="text-gray-600">Cargando datos...</p>
      </div>

      <!-- Main Content -->
      <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Delegados List -->
        <div class="lg:col-span-1">
          <div class="bg-white rounded-lg shadow-md p-4">
            <h2 class="text-xl font-bold text-gray-800 mb-4">Delegados</h2>
            <div class="space-y-2">
              <div
                v-for="delegado in delegados"
                :key="delegado.id"
                @click="seleccionar_delegado(delegado)"
                :class="[
                  'p-3 rounded cursor-pointer transition border-l-4',
                  delegadoSeleccionado?.id === delegado.id
                    ? 'bg-blue-100 border-blue-600'
                    : 'bg-gray-50 border-gray-300 hover:bg-gray-100'
                ]"
              >
                <p class="font-semibold text-gray-800">{{ delegado.nombre }}</p>
                <p class="text-sm text-gray-600">{{ delegado.cedula }}</p>
                <p class="text-xs text-gray-500 mt-1">
                  📍 {{ contarJuntasAsignadas(delegado.id) }} juntas
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Juntas Assignment -->
        <div class="lg:col-span-2">
          <div class="bg-white rounded-lg shadow-md p-6">
            <h2 class="text-xl font-bold text-gray-800 mb-4">
              {{ delegadoSeleccionado ? 'Asignar Juntas a: ' + delegadoSeleccionado.nombre : 'Selecciona un delegado' }}
            </h2>

            <div v-if="delegadoSeleccionado">
              <!-- Search -->
              <div class="mb-4">
                <input
                  v-model="filtroJunta"
                  type="text"
                  placeholder="Buscar junta por nombre o recinto..."
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <!-- Juntas Table -->
              <div class="overflow-x-auto">
                <table class="w-full">
                  <thead class="bg-gray-100 border-b border-gray-300">
                    <tr>
                      <th class="text-left px-4 py-3 font-semibold text-gray-700">Junta</th>
                      <th class="text-left px-4 py-3 font-semibold text-gray-700">Recinto</th>
                      <th class="text-left px-4 py-3 font-semibold text-gray-700">Tipo</th>
                      <th class="text-left px-4 py-3 font-semibold text-gray-700">Votantes</th>
                      <th class="text-center px-4 py-3 font-semibold text-gray-700">Acción</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="junta in juntasFiltradas" :key="junta.id" class="border-b border-gray-200 hover:bg-gray-50">
                      <td class="px-4 py-3 text-gray-800">{{ junta.nombre }}</td>
                      <td class="px-4 py-3 text-gray-600">{{ junta.recinto_nombre }}</td>
                      <td class="px-4 py-3">
                        <span :class="junta.tipo === 'm' ? 'bg-blue-100 text-blue-800' : 'bg-pink-100 text-pink-800'" class="px-2 py-1 rounded text-sm font-semibold">
                          {{ junta.tipo === 'm' ? 'Masculino' : 'Femenino' }}
                        </span>
                      </td>
                      <td class="px-4 py-3 text-gray-600">{{ junta.nro_votantes }}</td>
                      <td class="px-4 py-3 text-center">
                        <button
                          v-if="!junta.asignada"
                          @click="asignar_junta(junta)"
                          class="bg-green-600 hover:bg-green-700 text-white px-3 py-1 rounded text-sm font-semibold transition"
                        >
                          Asignar
                        </button>
                        <button
                          v-else
                          @click="desasignar_junta(junta)"
                          class="bg-red-600 hover:bg-red-700 text-white px-3 py-1 rounded text-sm font-semibold transition"
                        >
                          Quitar
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <!-- Juntas Asignadas a este Delegado -->
              <div class="mt-6 pt-6 border-t border-gray-300">
                <h3 class="font-bold text-gray-800 mb-3">Juntas Asignadas a {{ delegadoSeleccionado.nombre }}</h3>
                <div v-if="juntasDelDelegado.length > 0" class="grid grid-cols-1 md:grid-cols-2 gap-3">
                  <div
                    v-for="junta in juntasDelDelegado"
                    :key="junta.id"
                    class="bg-green-50 border border-green-200 p-3 rounded"
                  >
                    <p class="font-semibold text-gray-800">{{ junta.nombre }}</p>
                    <p class="text-sm text-gray-600">{{ junta.recinto_nombre }}</p>
                  </div>
                </div>
                <p v-else class="text-gray-500 italic">No hay juntas asignadas aún</p>
              </div>
            </div>

            <div v-else class="text-center py-12 text-gray-500">
              Selecciona un delegado en la lista de la izquierda
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

interface Delegado {
  id: number
  nombre: string
  cedula: string
  rol: string
}

interface Junta {
  id: number
  nombre: string
  codigo: string
  numero: number
  tipo: string
  nro_votantes: number
  recinto_nombre: string
  delegado_id?: number
  asignada?: boolean
}

const delegados = ref<Delegado[]>([])
const juntas = ref<Junta[]>([])
const delegadoSeleccionado = ref<Delegado | null>(null)
const filtroJunta = ref('')
const loading = ref(true)
const error = ref('')
const successMessage = ref('')

const juntasDisponibles = computed(() => juntas.value.filter(j => !j.delegado_id))
const juntasAsignadas = computed(() => juntas.value.filter(j => j.delegado_id).length)

const juntasDelDelegado = computed(() => {
  if (!delegadoSeleccionado.value) return []
  return juntas.value.filter(j => j.delegado_id === delegadoSeleccionado.value?.id)
})

const juntasFiltradas = computed(() => {
  let filtered = juntas.value
  
  if (delegadoSeleccionado.value) {
    filtered = filtered.filter(j => !j.delegado_id)
  }
  
  if (filtroJunta.value) {
    const q = filtroJunta.value.toLowerCase()
    filtered = filtered.filter(j => 
      j.nombre.toLowerCase().includes(q) || 
      j.recinto_nombre.toLowerCase().includes(q)
    )
  }
  
  return filtered
})

const contarJuntasAsignadas = (delegadoId: number) => {
  return juntas.value.filter(j => j.delegado_id === delegadoId).length
}

const seleccionar_delegado = (delegado: Delegado) => {
  delegadoSeleccionado.value = delegado
}

const cargar_datos = async () => {
  try {
    loading.value = true
    error.value = ''
    
    const [delegadosRes, juntasRes] = await Promise.all([
      axios.get('http://localhost:8000/delegados/'),
      axios.get('http://localhost:8000/juntas/')
    ])
    
    delegados.value = delegadosRes.data.filter((d: Delegado) => d.rol === 'delegado')
    juntas.value = juntasRes.data.map((j: Junta) => ({
      ...j,
      asignada: !!j.delegado_id
    }))
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Error al cargar datos'
  } finally {
    loading.value = false
  }
}

const asignar_junta = async (junta: Junta) => {
  try {
    await axios.post(
      `http://localhost:8000/juntas/${junta.id}/asignar-delegado`,
      { delegado_id: delegadoSeleccionado.value?.id }
    )
    
    junta.delegado_id = delegadoSeleccionado.value?.id
    junta.asignada = true
    successMessage.value = `Junta ${junta.nombre} asignada a ${delegadoSeleccionado.value?.nombre}`
    setTimeout(() => { successMessage.value = '' }, 3000)
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Error al asignar junta'
  }
}

const desasignar_junta = async (junta: Junta) => {
  try {
    await axios.post(
      `http://localhost:8000/juntas/${junta.id}/desasignar-delegado`
    )
    
    junta.delegado_id = undefined
    junta.asignada = false
    successMessage.value = `Junta ${junta.nombre} desasignada`
    setTimeout(() => { successMessage.value = '' }, 3000)
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Error al desasignar junta'
  }
}

onMounted(() => {
  cargar_datos()
})
</script>
