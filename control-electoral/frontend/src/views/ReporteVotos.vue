<template>
  <div class="p-8 max-w-2xl mx-auto">
    <h2 class="text-2xl font-bold mb-6">{{ isDelegado ? 'Ingreso de Votos' : 'Reporte de Votos' }}</h2>

    <!-- Estados -->
    <div v-if="estadoJunta" class="mb-6 p-4 rounded-lg" :class="[
      estadoJunta === 'procesada' 
        ? 'bg-green-50 border border-green-200' 
        : 'bg-yellow-50 border border-yellow-200'
    ]">
      <p class="font-semibold" :class="[
        estadoJunta === 'procesada' ? 'text-green-800' : 'text-yellow-800'
      ]">
        <span v-if="estadoJunta === 'procesada'">✓ Esta junta ya fue procesada</span>
        <span v-else>⏳ Junta pendiente de procesar</span>
      </p>
      <p v-if="estadoJunta === 'procesada'" class="text-sm text-green-700 mt-1">
        Los datos se muestran en modo de lectura. Para cambiar, contacta al administrador.
      </p>
    </div>

    <!-- Formulario -->
    <form @submit.prevent="enviarReporte" class="space-y-4 bg-white p-6 rounded shadow">

      <!-- Selector de Junta -->
      <div v-if="juntas.length > 1 || isDelegado" class="mb-6 pb-6 border-b">
        <label class="block text-sm font-medium mb-2">
          Junta {{ isDelegado ? '(La que deseas reportar)' : '' }}
        </label>
        <select 
          v-model="juntaId" 
          :disabled="isDelegadoWithOneJunta || estadoJunta === 'procesada'"
          @change="cargarEstadoJunta"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
        >
          <option value="">Seleccione una junta...</option>
          <option v-for="j in juntas" :key="j.id" :value="j.id">
            {{ j.nombre }} — {{ j.recinto_nombre }} ({{ j.tipo === 'm' ? 'Masculino' : 'Femenino' }})
            <span v-if="j.estado === 'procesada'"> ✓ Procesada</span>
          </option>
        </select>
        <p v-if="isDelegadoWithOneJunta" class="text-xs text-gray-500 mt-1">
          (Junta fija - solo puede reportar esta)
        </p>
      </div>

      <!-- Candidatos -->
      <div v-if="votos.length" class="space-y-3">
        <p class="text-sm font-medium text-gray-700">Votos por candidato:</p>
        <div v-for="(v, i) in votos" :key="i" class="flex gap-3 items-center">
          <span class="flex-1 text-sm font-medium">{{ v.nombre }}</span>
          <input 
            v-model.number="v.nro_votos" 
            type="number" 
            min="0" 
            :disabled="estadoJunta === 'procesada' || !juntaId"
            class="w-32 px-3 py-1 border border-gray-300 rounded text-right focus:outline-none focus:ring-2 focus:ring-blue-400 disabled:bg-gray-100"
            required 
          />
        </div>
      </div>

      <!-- Nulos y Blancos -->
      <div class="grid grid-cols-2 gap-4">
        <label class="block text-sm font-medium">
          Votos Nulos
          <input 
            v-model.number="nulos" 
            type="number" 
            min="0" 
            :disabled="estadoJunta === 'procesada' || !juntaId"
            class="w-full mt-1 px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400 disabled:bg-gray-100"
            required 
          />
        </label>
        <label class="block text-sm font-medium">
          Votos en Blanco
          <input 
            v-model.number="blancos" 
            type="number" 
            min="0" 
            :disabled="estadoJunta === 'procesada' || !juntaId"
            class="w-full mt-1 px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400 disabled:bg-gray-100"
            required 
          />
        </label>
      </div>

      <!-- Total Votantes -->
      <label class="block text-sm font-medium">
        Total Votantes (padrón de la junta)
        <input 
          v-model.number="totalVotantes" 
          type="number" 
          min="0" 
          :disabled="estadoJunta === 'procesada' || !juntaId"
          class="w-full mt-1 px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400 disabled:bg-gray-100"
          required 
        />
      </label>

      <!-- Botones -->
      <div class="flex gap-3 pt-4">
        <button 
          v-if="estadoJunta !== 'procesada'"
          type="submit" 
          :disabled="!juntaId || enviando" 
          class="flex-1 px-4 py-2 bg-blue-600 text-white font-semibold rounded hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ enviando ? 'Enviando...' : 'Guardar Reporte' }}
        </button>
        <button 
          v-else
          type="button" 
          @click="cambiarJunta"
          v-if="juntas.length > 1"
          class="flex-1 px-4 py-2 bg-gray-600 text-white font-semibold rounded hover:bg-gray-700 transition"
        >
          Cambiar de Junta
        </button>
      </div>

      <!-- Mensajes -->
      <div v-if="error" class="text-red-600 text-sm bg-red-50 p-3 rounded border border-red-200">
        {{ error }}
      </div>
      <div v-if="ok" class="text-green-700 text-sm bg-green-50 p-3 rounded border border-green-200">
        ✓ Reporte guardado correctamente y junta marcada como procesada
      </div>
    </form>

    <!-- Modal para cambiar junta -->
    <div v-if="mostrarModalCambio" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-md w-full mx-4">
        <h3 class="text-lg font-bold mb-4">Seleccionar otra junta</h3>
        <select 
          v-model="juntaIdCambio"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 mb-4"
        >
          <option value="">Seleccione...</option>
          <option v-for="j in juntas" :key="j.id" :value="j.id">
            {{ j.nombre }} ({{ j.estado }})
          </option>
        </select>
        <div class="flex gap-3">
          <button
            @click="confirmarCambio"
            class="flex-1 px-4 py-2 bg-blue-600 text-white font-semibold rounded hover:bg-blue-700 transition"
          >
            Continuar
          </button>
          <button
            @click="mostrarModalCambio = false"
            class="flex-1 px-4 py-2 bg-gray-300 text-gray-800 font-semibold rounded hover:bg-gray-400 transition"
          >
            Cancelar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue'
import axios from 'axios'

interface JuntaItem { 
  id: number
  nombre: string
  tipo: string
  recinto_nombre: string
  nro_votantes: number
  estado?: string
  delegado_id?: number
}

const juntas = ref<JuntaItem[]>([])
const juntaId = ref<number | ''>('')
const juntaIdCambio = ref<number | ''>('')
const votos = ref<{candidato_id:number, nombre:string, nro_votos:number}[]>([])
const nulos = ref(0)
const blancos = ref(0)
const totalVotantes = ref(0)
const error = ref('')
const ok = ref(false)
const enviando = ref(false)
const userRol = ref('')
const estadoJunta = ref<string>('')
const mostrarModalCambio = ref(false)

// Detectar si es delegado con una sola junta
const isDelegado = computed(() => userRol.value === 'delegado')
const isDelegadoWithOneJunta = computed(() => {
  return isDelegado.value && juntas.value.length === 1
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

const cargarEstadoJunta = async () => {
  estadoJunta.value = ''
  error.value = ''
  ok.value = false
  votos.value = []
  nulos.value = 0
  blancos.value = 0
  totalVotantes.value = 0

  if (!juntaId.value) return

  try {
    // Obtener estado de la junta
    const juntaRes = await axios.get(`/api/juntas/${juntaId.value}`)
    const junta = juntaRes.data
    estadoJunta.value = junta.estado || 'pendiente'

    // Cargar candidatos
    const candidatosRes = await axios.get('/api/partidos/candidatos/')
    votos.value = candidatosRes.data.map((c: any) => ({ 
      candidato_id: c.id, 
      nombre: c.nombre, 
      nro_votos: 0 
    }))

    // Pre-cargar nro_votantes
    const juntaSelec = juntas.value.find(j => j.id === juntaId.value)
    if (juntaSelec) totalVotantes.value = juntaSelec.nro_votantes

    // Si junta está procesada, cargar votos existentes
    if (estadoJunta.value === 'procesada') {
      try {
        const votosRes = await axios.get(`/api/votos/junta/${juntaId.value}`)
        for (const voto of votosRes.data) {
          const idx = votos.value.findIndex(v => v.candidato_id === voto.candidato_id)
          if (idx >= 0) {
            votos.value[idx].nro_votos = voto.nro_votos
          }
        }

        // Cargar resumen
        try {
          const resumenRes = await axios.get(`/api/votos/resumen/${juntaId.value}`)
          nulos.value = resumenRes.data.votos_nulos
          blancos.value = resumenRes.data.votos_blancos
          totalVotantes.value = resumenRes.data.total_votantes
        } catch {}
      } catch {}
    }
  } catch {
    error.value = 'Error al cargar datos de la junta'
  }
}

onMounted(async () => {
  try {
    userRol.value = getRol()
    
    // Cargar juntas según rol
    let juntasRes
    if (userRol.value === 'delegado') {
      juntasRes = await axios.get('/api/juntas/mis-juntas')
    } else {
      juntasRes = await axios.get('/api/juntas/')
    }
    
    const recintosRes = await axios.get('/api/recintos/')
    const recintoMap: Record<number, string> = {}
    for (const r of recintosRes.data) recintoMap[r.id] = r.nombre
    
    juntas.value = juntasRes.data.map((j: any) => ({
      ...j,
      recinto_nombre: recintoMap[j.recinto_id] || `Recinto ${j.recinto_id}`,
    }))
    
    // Si delegado con 1 junta, seleccionar automáticamente
    if (isDelegado.value && juntas.value.length === 1) {
      juntaId.value = juntas.value[0].id
      await cargarEstadoJunta()
    }
  } catch {
    error.value = 'Error al cargar juntas'
  }
})

watch(juntaId, async (val) => {
  if (val) {
    await cargarEstadoJunta()
  }
})

const cambiarJunta = () => {
  mostrarModalCambio.value = true
}

const confirmarCambio = () => {
  if (juntaIdCambio.value) {
    juntaId.value = juntaIdCambio.value as number
    juntaIdCambio.value = ''
    mostrarModalCambio.value = false
  }
}

async function enviarReporte() {
  error.value = ''
  ok.value = false
  enviando.value = true

  if (estadoJunta.value === 'procesada') {
    error.value = 'Esta junta ya fue procesada. No se puede modificar.'
    enviando.value = false
    return
  }

  try {
    // Enviar votos por candidato (upsert en backend)
    for (const v of votos.value) {
      await axios.post('/api/votos/', {
        junta_id: juntaId.value,
        candidato_id: v.candidato_id,
        nro_votos: v.nro_votos,
      })
    }

    // Enviar resumen de nulos y blancos
    await axios.post('/api/votos/resumen/', {
      junta_id: juntaId.value,
      votos_nulos: nulos.value,
      votos_blancos: blancos.value,
      total_votantes: totalVotantes.value,
    })

    // Marcar junta como procesada
    await axios.post(`/api/juntas/${juntaId.value}/marcar-procesada`)

    ok.value = true
    estadoJunta.value = 'procesada'

    // Recargar juntas para actualizar estados
    const juntasRes = await axios.get(
      isDelegado.value 
        ? '/api/juntas/mis-juntas'
        : '/api/juntas/'
    )
    const recintoMap: Record<number, string> = {}
    const recintosRes = await axios.get('/api/recintos/')
    for (const r of recintosRes.data) recintoMap[r.id] = r.nombre
    
    juntas.value = juntasRes.data.map((j: any) => ({
      ...j,
      recinto_nombre: recintoMap[j.recinto_id] || `Recinto ${j.recinto_id}`,
    }))
  } catch (e: any) {
    error.value = e.response?.data?.detail || 'Error al enviar reporte'
  } finally {
    enviando.value = false
  }
}
</script>
