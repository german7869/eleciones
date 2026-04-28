<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex justify-between items-center">
      <h1 class="text-3xl font-bold text-gray-800">Asignar Delegados a Juntas</h1>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div class="bg-blue-50 p-4 rounded-lg border border-blue-200">
        <p class="text-sm text-blue-600 font-semibold">Juntas sin delegado</p>
        <p class="text-2xl font-bold text-blue-800">{{ juntasSinDelegado.length }}</p>
      </div>
      <div class="bg-green-50 p-4 rounded-lg border border-green-200">
        <p class="text-sm text-green-600 font-semibold">Delegados disponibles</p>
        <p class="text-2xl font-bold text-green-800">{{ delegados.length }}</p>
      </div>
      <div class="bg-purple-50 p-4 rounded-lg border border-purple-200">
        <p class="text-sm text-purple-600 font-semibold">Asignaciones hechas</p>
        <p class="text-2xl font-bold text-purple-800">{{ asignacionesHechas }}</p>
      </div>
    </div>

    <!-- Asignación Form -->
    <div class="bg-white p-6 rounded-lg shadow-md border border-gray-200">
      <h2 class="text-xl font-bold text-gray-800 mb-4">Nueva Asignación</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-2">Seleccionar Junta</label>
          <select 
            v-model="juntaSeleccionada"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">-- Selecciona una junta --</option>
            <option v-for="junta in juntasSinDelegado" :key="junta.id" :value="junta.id">
              {{ junta.nombre }} ({{ junta.recinto_nombre }})
            </option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-2">Seleccionar Delegado</label>
          <select 
            v-model="delegadoSeleccionado"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
          >
            <option value="">-- Selecciona un delegado --</option>
            <option v-for="delegado in delegados" :key="delegado.id" :value="delegado.id">
              {{ delegado.nombre }} ({{ delegado.cedula }}) - {{ delegado.juntas_asignadas }} juntas
            </option>
          </select>
        </div>
        <div class="flex items-end gap-2">
          <button 
            @click="asignarDelegado"
            :disabled="!juntaSeleccionada || !delegadoSeleccionado"
            class="flex-1 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 font-semibold"
          >
            ✓ Asignar
          </button>
          <button 
            @click="limpiarSeleccion"
            class="px-3 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
          >
            Limpiar
          </button>
        </div>
      </div>
    </div>

    <!-- Juntas sin delegado -->
    <div class="bg-white p-6 rounded-lg shadow-md border border-gray-200">
      <h2 class="text-xl font-bold text-gray-800 mb-4">Juntas sin Delegado ({{ juntasSinDelegado.length }})</h2>
      
      <div v-if="juntasSinDelegado.length === 0" class="text-center py-8 text-gray-500">
        ✅ Todas las juntas tienen delegado asignado
      </div>
      
      <div v-else class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-100">
            <tr>
              <th class="px-4 py-2 text-left text-sm font-semibold text-gray-700">Código</th>
              <th class="px-4 py-2 text-left text-sm font-semibold text-gray-700">Nombre</th>
              <th class="px-4 py-2 text-left text-sm font-semibold text-gray-700">Recinto</th>
              <th class="px-4 py-2 text-left text-sm font-semibold text-gray-700">Tipo</th>
              <th class="px-4 py-2 text-center text-sm font-semibold text-gray-700">Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="junta in juntasSinDelegado" :key="junta.id" class="border-b hover:bg-gray-50">
              <td class="px-4 py-2 text-sm text-gray-900">{{ junta.codigo }}</td>
              <td class="px-4 py-2 text-sm text-gray-900 font-medium">{{ junta.nombre }}</td>
              <td class="px-4 py-2 text-sm text-gray-600">{{ junta.recinto_nombre }}</td>
              <td class="px-4 py-2 text-sm">
                <span v-if="junta.tipo === 'm'" class="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs font-semibold">M</span>
                <span v-else class="bg-pink-100 text-pink-800 px-2 py-1 rounded text-xs font-semibold">F</span>
              </td>
              <td class="px-4 py-2 text-center">
                <select 
                  class="text-xs px-2 py-1 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                  @change="(evt) => asignarDelegadoRapido(junta.id, evt.target.value)"
                >
                  <option value="">Asignar delegado</option>
                  <option v-for="delegado in delegados" :key="delegado.id" :value="delegado.id">
                    {{ delegado.nombre }}
                  </option>
                </select>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Toast Notification -->
    <Toast />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useToast } from '@/composables/useToast'
import Toast from '@/components/Toast.vue'
import axios from 'axios'

const toast = useToast()

const juntasSinDelegado = ref<any[]>([])
const delegados = ref<any[]>([])
const juntaSeleccionada = ref('')
const delegadoSeleccionado = ref('')
const asignacionesHechas = ref(0)

const cargarDatos = async () => {
  try {
    const [juntasRes, delegadosRes] = await Promise.all([
      axios.get('/juntas/listar-juntas-sin-delegado'),
      axios.get('/juntas/listar-delegados-disponibles')
    ])
    juntasSinDelegado.value = juntasRes.data
    delegados.value = delegadosRes.data
  } catch (error) {
    toast.error('Error al cargar datos')
    console.error(error)
  }
}

const asignarDelegado = async () => {
  if (!juntaSeleccionada.value || !delegadoSeleccionado.value) {
    toast.warning('Selecciona una junta y un delegado')
    return
  }

  try {
    await axios.post('/juntas/asignar-delegado', {
      junta_id: parseInt(juntaSeleccionada.value),
      delegado_id: parseInt(delegadoSeleccionado.value)
    })
    toast.success('Delegado asignado correctamente')
    asignacionesHechas.value++
    limpiarSeleccion()
    await cargarDatos()
  } catch (error: any) {
    toast.error(error.response?.data?.detail || 'Error al asignar')
    console.error(error)
  }
}

const asignarDelegadoRapido = async (juntaId: number, delegadoId: string) => {
  if (!delegadoId) return
  try {
    await axios.post('/juntas/asignar-delegado', {
      junta_id: juntaId,
      delegado_id: parseInt(delegadoId)
    })
    toast.success('Delegado asignado')
    asignacionesHechas.value++
    await cargarDatos()
  } catch (error: any) {
    toast.error(error.response?.data?.detail || 'Error al asignar')
  }
}

const limpiarSeleccion = () => {
  juntaSeleccionada.value = ''
  delegadoSeleccionado.value = ''
}

onMounted(() => {
  cargarDatos()
})
</script>
