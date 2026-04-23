<template>
  <div class="p-8 max-w-lg mx-auto">
    <h2 class="text-xl font-bold mb-4">Reporte de Votos</h2>
    <form @submit.prevent="enviarReporte" class="space-y-4 bg-white p-6 rounded shadow">
      <label class="block">
        ID de Junta:
        <input v-model="juntaId" type="number" class="input w-full mt-1" required />
      </label>
      <div v-for="(v, i) in votos" :key="i" class="flex gap-2 items-center">
        <span class="w-32">{{ v.nombre }}</span>
        <input v-model.number="v.nro_votos" type="number" min="0" class="input w-24" required />
      </div>
      <label class="block">
        Votos Nulos:
        <input v-model.number="nulos" type="number" min="0" class="input w-full mt-1" required />
      </label>
      <label class="block">
        Votos en Blanco:
        <input v-model.number="blancos" type="number" min="0" class="input w-full mt-1" required />
      </label>
      <button type="submit" class="btn bg-blue-600 text-white w-full">Enviar Reporte</button>
      <div v-if="error" class="text-red-600 mt-2">{{ error }}</div>
      <div v-if="ok" class="text-green-700 mt-2">Reporte enviado correctamente</div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import axios from 'axios';

const juntaId = ref('');
const votos = ref<{candidato_id:number, nombre:string, nro_votos:number}[]>([]);
const nulos = ref(0);
const blancos = ref(0);
const error = ref('');
const ok = ref(false);

watch(juntaId, async (val) => {
  votos.value = [];
  ok.value = false;
  error.value = '';
  if (!val) return;
  try {
    // Obtener candidatos (puedes filtrar por junta si el backend lo permite)
    const res = await axios.get('/partidos/candidatos/');
    votos.value = res.data.map((c:any) => ({ candidato_id: c.id, nombre: c.nombre, nro_votos: 0 }));
  } catch {
    error.value = 'No se pudieron cargar candidatos';
  }
});

async function enviarReporte() {
  error.value = '';
  ok.value = false;
  if (!juntaId.value) {
    error.value = 'Debe ingresar el ID de la junta';
    return;
  }
  try {
    for (const v of votos.value) {
      await axios.post('/votos/', {
        junta_id: juntaId.value,
        candidato_id: v.candidato_id,
        nro_votos: v.nro_votos
      });
    }
    // Registrar nulos y blancos como candidatos especiales si existen en el backend
    ok.value = true;
  } catch (e: any) {
    error.value = e.response?.data?.detail || 'Error al enviar reporte';
  }
}
</script>
