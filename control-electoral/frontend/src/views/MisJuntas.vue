<template>
  <div class="p-6">
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900">Mis Juntas Asignadas</h1>
      <p class="text-gray-600 mt-2">Juntas bajo su responsabilidad como delegado</p>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
      <div class="bg-blue-50 rounded-lg p-6 border border-blue-200">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-blue-600 text-sm font-semibold">Total de Juntas</p>
            <p class="text-3xl font-bold text-blue-900 mt-2">{{ juntas.length }}</p>
          </div>
          <div class="bg-blue-200 rounded-full p-3">
            <svg class="w-6 h-6 text-blue-900" fill="currentColor" viewBox="0 0 20 20">
              <path d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v4h8v-4zM6 8a2 2 0 11-4 0 2 2 0 014 0zM16 18v-3a5.972 5.972 0 00-.75-2.906A3.005 3.005 0 0119 15v3h-3zM4.75 12.094A5.973 5.973 0 004 15v3H1v-3a3 3 0 013.75-2.906z"></path>
            </svg>
          </div>
        </div>
      </div>

      <div class="bg-green-50 rounded-lg p-6 border border-green-200">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-green-600 text-sm font-semibold">Juntas Procesadas</p>
            <p class="text-3xl font-bold text-green-900 mt-2">{{ juntasProcesadas }}</p>
          </div>
          <div class="bg-green-200 rounded-full p-3">
            <svg class="w-6 h-6 text-green-900" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- Tabla de juntas -->
    <div class="bg-white rounded-lg shadow overflow-hidden">
      <div class="px-6 py-4 bg-gray-50 border-b border-gray-200">
        <h2 class="text-lg font-semibold text-gray-900">Detalle de Juntas</h2>
      </div>

      <div v-if="loading" class="p-6 text-center text-gray-600">
        Cargando juntas...
      </div>

      <div v-else-if="juntas.length === 0" class="p-6 text-center text-gray-600">
        <svg class="w-12 h-12 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"></path>
        </svg>
        <p>No tiene juntas asignadas</p>
      </div>

      <table v-else class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Código</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nombre</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Recinto</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Tipo</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Votantes</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Acciones</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="junta in juntas" :key="junta.id" class="hover:bg-gray-50 transition">
            <td class="px-6 py-4 whitespace-nowrap text-sm font-semibold text-gray-900">{{ junta.codigo }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{{ junta.nombre }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{{ junta.recinto_nombre }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm">
              <span v-if="junta.tipo === 'm'" class="px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800">
                Masculina
              </span>
              <span v-else class="px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full bg-pink-100 text-pink-800">
                Femenina
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{{ junta.nro_votantes }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm space-x-2">
              <button @click="cargarAccionesJunta(junta)" class="text-blue-600 hover:text-blue-900 font-semibold">
                Subir Acta
              </button>
              <button @click="verResultados(junta)" class="text-green-600 hover:text-green-900 font-semibold">
                Ver Resultados
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal para subir acta -->
    <div v-if="showUploadModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-md w-full mx-4">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Subir Acta - {{ juntaSeleccionada?.nombre }}</h3>
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-2">Archivo PDF</label>
          <input type="file" accept=".pdf" @change="handleFileUpload" class="block w-full text-sm text-gray-500" />
        </div>
        <div class="flex space-x-2 justify-end">
          <button @click="showUploadModal = false" class="px-4 py-2 text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50">
            Cancelar
          </button>
          <button @click="subirAccta" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
            Enviar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useToast } from '@/composables/useToast'

const { toasts, success, error } = useToast()

interface Junta {
  id: number
  codigo: string
  nombre: string
  recinto_nombre: string
  recinto_id: number
  tipo: string
  nro_votantes: number
}

const juntas = ref<Junta[]>([])
const loading = ref(true)
const showUploadModal = ref(false)
const juntaSeleccionada = ref<Junta | null>(null)
const fileSeleccionado = ref<File | null>(null)
const juntasProcesadas = ref(0)

const cargarJuntas = async () => {
  try {
    loading.value = true
    const response = await axios.get('/api/juntas/mis-juntas')
    juntas.value = response.data
  } catch (err: any) {
    error('Error al cargar juntas: ' + (err.response?.data?.detail || err.message))
  } finally {
    loading.value = false
  }
}

const cargarAccionesJunta = (junta: Junta) => {
  juntaSeleccionada.value = junta
  showUploadModal.value = true
}

const handleFileUpload = (event: Event) => {
  const input = event.target as HTMLInputElement
  if (input.files?.[0]) {
    fileSeleccionado.value = input.files[0]
  }
}

const subirAccta = async () => {
  if (!juntaSeleccionada.value || !fileSeleccionado.value) {
    error('Debe seleccionar un archivo')
    return
  }

  try {
    const formData = new FormData()
    formData.append('file', fileSeleccionado.value)
    formData.append('junta_id', String(juntaSeleccionada.value.id))

    const response = await axios.post('/api/upload-acta', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })

    success('Acta subida correctamente')
    juntasProcesadas.value++
    showUploadModal.value = false
  } catch (err: any) {
    error('Error al subir acta: ' + (err.response?.data?.detail || err.message))
  }
}

const verResultados = (junta: Junta) => {
  success('Redirigiendo a resultados...')
}

onMounted(() => {
  cargarJuntas()
})
</script>
