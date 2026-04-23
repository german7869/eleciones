<template>
  <div class="p-8 max-w-2xl mx-auto">
    <h2 class="text-xl font-bold mb-4">Resultados Generales</h2>
    <div class="mb-4 flex gap-4 flex-wrap">
      <label>Filtrar por parroquia:
        <select v-model="parroquiaId" class="input ml-2">
          <option value="">Todas</option>
          <option v-for="p in parroquias" :key="p.id" :value="p.id">{{ p.nombre }}</option>
        </select>
      </label>
      <label v-if="zonas.length">
        Zona:
        <select v-model="zonaId" class="input ml-2">
          <option value="">Todas</option>
          <option v-for="z in zonas" :key="z.id" :value="z.id">{{ z.nombre }}</option>
        </select>
      </label>
      <label v-if="recintos.length">
        Recinto:
        <select v-model="recintoId" class="input ml-2">
          <option value="">Todos</option>
          <option v-for="r in recintos" :key="r.id" :value="r.id">{{ r.nombre }}</option>
        </select>
      </label>
    </div>
    <div v-if="loading" class="text-gray-500">Cargando...</div>
    <div v-else>
      <table class="min-w-full bg-white rounded shadow mb-6">
        <thead>
          <tr>
            <th class="p-2 text-left">Candidato</th>
            <th class="p-2 text-right">Votos</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="r in resultados" :key="r.candidato_id">
            <td class="p-2">{{ r.nombre }}</td>
            <td class="p-2 text-right">{{ r.votos }}</td>
          </tr>
        </tbody>
      </table>
      <div class="bg-gray-100 p-4 rounded">
        <BarChart :labels="resultados.map(r => r.nombre)" :data="resultados.map(r => r.votos)" />
      </div>
    </div>
  </div>
</template>

</script>
<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import axios from 'axios';
import BarChart from '../components/BarChart.vue';

const resultados = ref<{candidato_id:number, nombre:string, votos:number}[]>([]);
const loading = ref(true);
const parroquias = ref<{id:number, nombre:string}[]>([]);
const zonas = ref<{id:number, nombre:string, parroquia_id:number}[]>([]);
const recintos = ref<{id:number, nombre:string, zona_id:number}[]>([]);
const parroquiaId = ref<string | number>('');
const zonaId = ref<string | number>('');
const recintoId = ref<string | number>('');

async function cargarResultados() {
  loading.value = true;
  try {
    const candidatos = await axios.get('/partidos/candidatos/');
    const votos = await axios.get('/votos/');
    let votosFiltrados = votos.data;
    let zonasIds: number[] = [];
    if (parroquiaId.value) {
      const zonasRes = await axios.get(`/zonas?parroquia_id=${parroquiaId.value}`);
      zonas.value = zonasRes.data;
      zonasIds = zonas.value.map((z:any) => z.id);
    } else {
      const zonasRes = await axios.get('/zonas/');
      zonas.value = zonasRes.data;
      zonasIds = zonas.value.map((z:any) => z.id);
    }
    let recintosData = (await axios.get('/recintos/')).data;
    if (zonaId.value) {
      recintos.value = recintosData.filter((r:any) => r.zona_id == zonaId.value);
    } else if (parroquiaId.value) {
      recintos.value = recintosData.filter((r:any) => zonasIds.includes(r.zona_id));
    } else {
      recintos.value = recintosData;
    }
    let juntasIds: number[] = [];
    if (recintoId.value) {
      juntasIds = (await axios.get('/juntas/')).data.filter((j:any) => j.recinto_id == recintoId.value).map((j:any) => j.id);
      votosFiltrados = votos.data.filter((v:any) => juntasIds.includes(v.junta_id));
    } else if (zonaId.value) {
      const recintosIds = recintos.value.map((r:any) => r.id);
      juntasIds = (await axios.get('/juntas/')).data.filter((j:any) => recintosIds.includes(j.recinto_id)).map((j:any) => j.id);
      votosFiltrados = votos.data.filter((v:any) => juntasIds.includes(v.junta_id));
    } else if (parroquiaId.value) {
      const recintosIds = recintos.value.map((r:any) => r.id);
      juntasIds = (await axios.get('/juntas/')).data.filter((j:any) => recintosIds.includes(j.recinto_id)).map((j:any) => j.id);
      votosFiltrados = votos.data.filter((v:any) => juntasIds.includes(v.junta_id));
    }
    resultados.value = candidatos.data.map((c:any) => ({
      candidato_id: c.id,
      nombre: c.nombre,
      votos: votosFiltrados.filter((v:any) => v.candidato_id === c.id).reduce((a:number, v:any) => a + v.nro_votos, 0)
    }));
  } catch {
    resultados.value = [];
  }
  loading.value = false;
}

onMounted(async () => {
  const parroq = await axios.get('/parroquias/');
  parroquias.value = parroq.data;
  await cargarResultados();
});

watch([parroquiaId, zonaId, recintoId], async () => {
  await cargarResultados();
});
</script>
</script>
