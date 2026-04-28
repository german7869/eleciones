<template>
  <div class="p-8 max-w-3xl mx-auto">
    <h2 class="text-xl font-bold mb-4">Resultados Generales</h2>

    <div class="mb-4 flex gap-4 flex-wrap items-end">
      <label class="flex flex-col text-sm">
        Parroquia
        <select v-model="parroquiaId" class="input mt-1">
          <option value="">Todas</option>
          <option v-for="p in parroquias" :key="p.id" :value="p.id">{{ p.nombre }}</option>
        </select>
      </label>
      <label v-if="zonas.length" class="flex flex-col text-sm">
        Zona
        <select v-model="zonaId" class="input mt-1">
          <option value="">Todas</option>
          <option v-for="z in zonas" :key="z.id" :value="z.id">{{ z.nombre }}</option>
        </select>
      </label>
      <label v-if="recintos.length" class="flex flex-col text-sm">
        Recinto
        <select v-model="recintoId" class="input mt-1">
          <option value="">Todos</option>
          <option v-for="r in recintos" :key="r.id" :value="r.id">{{ r.nombre }}</option>
        </select>
      </label>
    </div>

    <div v-if="loading" class="text-gray-500">Cargando...</div>
    <div v-else>
      <table class="min-w-full bg-white rounded shadow mb-4">
        <thead class="bg-blue-600 text-white">
          <tr>
            <th class="p-2 text-left">Candidato</th>
            <th class="p-2 text-left">Partido</th>
            <th class="p-2 text-right">Votos</th>
            <th class="p-2 text-right">%</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="r in candidatos" :key="r.candidato_id" class="border-b">
            <td class="p-2">{{ r.candidato }}</td>
            <td class="p-2 text-gray-500 text-sm">{{ r.partido }}</td>
            <td class="p-2 text-right font-mono">{{ r.total_votos }}</td>
            <td class="p-2 text-right font-mono">{{ r.porcentaje }}%</td>
          </tr>
        </tbody>
      </table>

      <div class="bg-white rounded shadow p-4 mb-4 grid grid-cols-2 gap-3 text-sm">
        <div class="text-gray-600">Votos válidos: <span class="font-bold text-gray-900">{{ totales.votos_validos }}</span></div>
        <div class="text-gray-600">Votos nulos: <span class="font-bold text-gray-900">{{ totales.votos_nulos }}</span></div>
        <div class="text-gray-600">Votos en blanco: <span class="font-bold text-gray-900">{{ totales.votos_blancos }}</span></div>
        <div class="text-gray-600">Total emitidos: <span class="font-bold text-gray-900">{{ totales.total_emitidos }}</span></div>
        <div class="text-gray-600">Padrón: <span class="font-bold text-gray-900">{{ totales.total_votantes }}</span></div>
        <div class="text-gray-600">Participación: <span class="font-bold text-blue-600">{{ totales.participacion_pct }}%</span></div>
      </div>

      <div class="bg-gray-100 p-4 rounded">
        <BarChart :labels="candidatos.map(r => r.candidato)" :data="candidatos.map(r => r.total_votos)" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import axios from 'axios';
import BarChart from '../components/BarChart.vue';

const loading = ref(true);
const parroquias = ref<{id:number, nombre:string}[]>([]);
const zonas = ref<{id:number, nombre:string}[]>([]);
const recintos = ref<{id:number, nombre:string}[]>([]);
const parroquiaId = ref<number|''>('');
const zonaId = ref<number|''>('');
const recintoId = ref<number|''>('');

const candidatos = ref<{candidato_id:number, candidato:string, partido:string, total_votos:number, porcentaje:number}[]>([]);
const totales = ref({ votos_validos:0, votos_nulos:0, votos_blancos:0, total_emitidos:0, total_votantes:0, participacion_pct:0 });

async function cargarFiltros() {
  if (parroquiaId.value) {
    zonas.value = (await axios.get('/zonas/', { params: { parroquia_id: parroquiaId.value } })).data;
    zonaId.value = '';
    recintoId.value = '';
    recintos.value = [];
  } else {
    zonas.value = [];
    recintos.value = [];
    zonaId.value = '';
    recintoId.value = '';
  }
}

async function cargarRecintos() {
  if (zonaId.value) {
    recintos.value = (await axios.get('/recintos/', { params: { zona_id: zonaId.value } })).data;
    recintoId.value = '';
  } else {
    recintos.value = [];
    recintoId.value = '';
  }
}

async function cargarResultados() {
  loading.value = true;
  try {
    const params: Record<string, any> = {};
    if (parroquiaId.value) params.parroquia_id = parroquiaId.value;
    if (zonaId.value) params.zona_id = zonaId.value;
    if (recintoId.value) params.recinto_id = recintoId.value;
    const res = await axios.get('/resultados/', { params });
    candidatos.value = res.data.candidatos;
    totales.value = res.data.totales;
  } catch {
    candidatos.value = [];
  }
  loading.value = false;
}

onMounted(async () => {
  parroquias.value = (await axios.get('/parroquias/')).data;
  await cargarResultados();
});

watch(parroquiaId, async () => { await cargarFiltros(); await cargarResultados(); });
watch(zonaId, async () => { await cargarRecintos(); await cargarResultados(); });
watch(recintoId, cargarResultados);
</script>
