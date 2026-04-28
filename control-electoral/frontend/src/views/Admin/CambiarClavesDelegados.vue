<template>
  <div class="min-h-screen bg-gray-50 p-6">
    <div class="max-w-6xl mx-auto">
      <div class="bg-white rounded-lg shadow-md p-6">
        <h1 class="text-3xl font-bold text-gray-800 mb-6">Cambiar Contraseñas de Delegados</h1>
        
        <!-- Error Alert -->
        <div v-if="error" class="bg-red-50 border border-red-200 text-red-800 px-4 py-3 rounded mb-4">
          {{ error }}
        </div>
        
        <!-- Success Alert -->
        <div v-if="successMessage" class="bg-green-50 border border-green-200 text-green-800 px-4 py-3 rounded mb-4">
          {{ successMessage }}
        </div>
        
        <!-- Loading -->
        <div v-if="loading" class="text-center py-12">
          <p class="text-gray-600">Cargando delegados...</p>
        </div>
        
        <!-- Delegados Table -->
        <div v-else-if="delegados.length > 0" class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-gray-100 border-b border-gray-300">
              <tr>
                <th class="text-left px-4 py-3 font-semibold text-gray-700">Nombre</th>
                <th class="text-left px-4 py-3 font-semibold text-gray-700">Cédula/Email</th>
                <th class="text-left px-4 py-3 font-semibold text-gray-700">Rol</th>
                <th class="text-left px-4 py-3 font-semibold text-gray-700">Acción</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="delegado in delegados" :key="delegado.id" class="border-b border-gray-200 hover:bg-gray-50">
                <td class="px-4 py-3 text-gray-800">{{ delegado.nombre }}</td>
                <td class="px-4 py-3 text-gray-600">{{ delegado.cedula }}</td>
                <td class="px-4 py-3">
                  <span :class="delegado.rol === 'admin' ? 'bg-red-100 text-red-800' : 'bg-blue-100 text-blue-800'" class="px-2 py-1 rounded text-sm font-semibold">
                    {{ delegado.rol }}
                  </span>
                </td>
                <td class="px-4 py-3">
                  <button
                    @click="abrir_modal(delegado)"
                    class="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded text-sm font-semibold transition"
                  >
                    Cambiar Clave
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <!-- Empty State -->
        <div v-else class="text-center py-12">
          <p class="text-gray-600 text-lg">No hay delegados registrados</p>
        </div>
      </div>
    </div>
    
    <!-- Modal para cambiar contraseña -->
    <div v-if="modalActivo" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 shadow-lg max-w-md w-full mx-4">
        <h2 class="text-2xl font-bold text-gray-800 mb-2">Cambiar Contraseña</h2>
        <p class="text-gray-600 mb-4">{{ delegadoSeleccionado?.nombre }}</p>
        
        <!-- Nueva Contraseña -->
        <div class="mb-4">
          <label class="block text-gray-700 font-semibold mb-2">Nueva Contraseña</label>
          <input
            v-model="nuevaClave"
            type="password"
            placeholder="Ingrese la nueva contraseña"
            class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <p class="text-gray-500 text-sm mt-1">Mínimo 6 caracteres</p>
        </div>
        
        <!-- Confirmar Contraseña -->
        <div class="mb-6">
          <label class="block text-gray-700 font-semibold mb-2">Confirmar Contraseña</label>
          <input
            v-model="confirmarClave"
            type="password"
            placeholder="Confirme la contraseña"
            class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        
        <!-- Modal Error -->
        <div v-if="modalError" class="bg-red-50 border border-red-200 text-red-800 px-3 py-2 rounded mb-4 text-sm">
          {{ modalError }}
        </div>
        
        <!-- Buttons -->
        <div class="flex gap-3 justify-end">
          <button
            @click="cerrar_modal"
            class="px-4 py-2 bg-gray-300 text-gray-800 rounded font-semibold hover:bg-gray-400 transition"
          >
            Cancelar
          </button>
          <button
            @click="guardar_nueva_clave"
            :disabled="guardando"
            class="px-4 py-2 bg-blue-600 text-white rounded font-semibold hover:bg-blue-700 transition disabled:opacity-50"
          >
            {{ guardando ? "Guardando..." : "Cambiar Contraseña" }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'

interface Delegado {
  id: number
  nombre: string
  cedula: string
  telefono?: string
  rol: string
}

const delegados = ref<Delegado[]>([])
const loading = ref(true)
const error = ref('')
const successMessage = ref('')
const modalActivo = ref(false)
const delegadoSeleccionado = ref<Delegado | null>(null)
const nuevaClave = ref('')
const confirmarClave = ref('')
const modalError = ref('')
const guardando = ref(false)

// Cargar delegados
const cargar_delegados = async () => {
  try {
    loading.value = true
    error.value = ''
    const response = await axios.get('http://localhost:8000/delegados/')
    delegados.value = response.data
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Error al cargar delegados'
  } finally {
    loading.value = false
  }
}

// Abrir modal
const abrir_modal = (delegado: Delegado) => {
  delegadoSeleccionado.value = delegado
  nuevaClave.value = ''
  confirmarClave.value = ''
  modalError.value = ''
  modalActivo.value = true
}

// Cerrar modal
const cerrar_modal = () => {
  modalActivo.value = false
  delegadoSeleccionado.value = null
  nuevaClave.value = ''
  confirmarClave.value = ''
  modalError.value = ''
}

// Guardar nueva contraseña
const guardar_nueva_clave = async () => {
  modalError.value = ''
  
  // Validaciones
  if (!nuevaClave.value || nuevaClave.value.trim().length === 0) {
    modalError.value = 'La contraseña no puede estar vacía'
    return
  }
  
  if (nuevaClave.value.length < 6) {
    modalError.value = 'La contraseña debe tener al menos 6 caracteres'
    return
  }
  
  if (nuevaClave.value !== confirmarClave.value) {
    modalError.value = 'Las contraseñas no coinciden'
    return
  }
  
  try {
    guardando.value = true
    await axios.post(
      `http://localhost:8000/delegados/${delegadoSeleccionado.value?.id}/cambiar-clave`,
      { nueva_clave: nuevaClave.value }
    )
    
    successMessage.value = `Contraseña de ${delegadoSeleccionado.value?.nombre} cambiada exitosamente`
    cerrar_modal()
    
    // Limpiar mensaje de éxito después de 3 segundos
    setTimeout(() => {
      successMessage.value = ''
    }, 3000)
    
  } catch (err: any) {
    modalError.value = err.response?.data?.detail || 'Error al cambiar contraseña'
  } finally {
    guardando.value = false
  }
}

onMounted(() => {
  cargar_delegados()
})
</script>
