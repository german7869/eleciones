<template>
  <div class="p-8 max-w-4xl mx-auto">
    <h2 class="text-xl font-bold mb-6">Gestión de Partidos y Candidatos</h2>

    <div class="grid md:grid-cols-2 gap-6">
      <!-- Partidos -->
      <div>
        <div class="flex justify-between items-center mb-2">
          <h3 class="font-semibold">Partidos</h3>
          <button @click="abrirModalPartido()" class="text-sm btn bg-blue-600 text-white px-3 py-1 rounded">+ Nuevo</button>
        </div>
        <table class="w-full bg-white rounded shadow text-sm">
          <thead class="bg-gray-100"><tr><th class="p-2 text-left">Código</th><th class="p-2 text-left">Nombre</th><th class="p-2"></th></tr></thead>
          <tbody>
            <tr v-for="p in partidos" :key="p.id" class="border-b cursor-pointer" :class="partidoSeleccionado?.id === p.id ? 'bg-blue-50' : ''" @click="seleccionarPartido(p)">
              <td class="p-2">{{ p.codigo }}</td>
              <td class="p-2">{{ p.nombre }}</td>
              <td class="p-2">
                <button @click.stop="eliminarPartido(p.id)" class="text-red-500 hover:underline">Eliminar</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Candidatos del partido seleccionado -->
      <div>
        <div class="flex justify-between items-center mb-2">
          <h3 class="font-semibold">Candidatos{{ partidoSeleccionado ? ` — ${partidoSeleccionado.nombre}` : '' }}</h3>
          <button v-if="partidoSeleccionado" @click="abrirModalCandidato()" class="text-sm btn bg-green-600 text-white px-3 py-1 rounded">+ Nuevo</button>
        </div>
        <p v-if="!partidoSeleccionado" class="text-gray-400 text-sm">Seleccione un partido</p>
        <table v-else class="w-full bg-white rounded shadow text-sm">
          <thead class="bg-gray-100"><tr><th class="p-2 text-left">#</th><th class="p-2 text-left">Nombre</th><th class="p-2"></th></tr></thead>
          <tbody>
            <tr v-for="c in candidatosFiltrados" :key="c.id" class="border-b">
              <td class="p-2">{{ c.orden_papeleta }}</td>
              <td class="p-2">{{ c.nombre }}</td>
              <td class="p-2"><button @click="eliminarCandidato(c.id)" class="text-red-500 hover:underline">Eliminar</button></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal Partido -->
    <div v-if="modalPartido" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div class="bg-white rounded shadow-lg p-6 w-80">
        <h3 class="font-bold mb-3">Nuevo Partido</h3>
        <form @submit.prevent="guardarPartido" class="space-y-2">
          <input v-model="formPartido.codigo" placeholder="Código" class="input w-full" required />
          <input v-model="formPartido.nombre" placeholder="Nombre" class="input w-full" required />
          <div v-if="errorPartido" class="text-red-600 text-sm">{{ errorPartido }}</div>
          <div class="flex gap-2 justify-end">
            <button type="button" @click="modalPartido=false" class="btn border px-3 py-1 rounded">Cancelar</button>
            <button type="submit" class="btn bg-blue-600 text-white px-3 py-1 rounded">Guardar</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal Candidato -->
    <div v-if="modalCandidato" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div class="bg-white rounded shadow-lg p-6 w-80">
        <h3 class="font-bold mb-3">Nuevo Candidato</h3>
        <form @submit.prevent="guardarCandidato" class="space-y-2">
          <input v-model="formCandidato.nombre" placeholder="Nombre" class="input w-full" required />
          <input v-model.number="formCandidato.orden_papeleta" type="number" placeholder="Orden en papeleta" class="input w-full" required />
          <div v-if="errorCandidato" class="text-red-600 text-sm">{{ errorCandidato }}</div>
          <div class="flex gap-2 justify-end">
            <button type="button" @click="modalCandidato=false" class="btn border px-3 py-1 rounded">Cancelar</button>
            <button type="submit" class="btn bg-green-600 text-white px-3 py-1 rounded">Guardar</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';

interface Partido { id: number; codigo: string; nombre: string }
interface Candidato { id: number; nombre: string; partido_id: number; orden_papeleta: number }

const partidos = ref<Partido[]>([]);
const candidatos = ref<Candidato[]>([]);
const partidoSeleccionado = ref<Partido | null>(null);
const modalPartido = ref(false);
const modalCandidato = ref(false);
const formPartido = ref({ codigo: '', nombre: '' });
const formCandidato = ref({ nombre: '', orden_papeleta: 1 });
const errorPartido = ref('');
const errorCandidato = ref('');

const candidatosFiltrados = computed(() =>
  candidatos.value.filter(c => c.partido_id === partidoSeleccionado.value?.id)
    .sort((a, b) => a.orden_papeleta - b.orden_papeleta)
);

async function cargar() {
  const [p, c] = await Promise.all([axios.get('/partidos/'), axios.get('/partidos/candidatos/')]);
  partidos.value = p.data;
  candidatos.value = c.data;
}

function seleccionarPartido(p: Partido) { partidoSeleccionado.value = p; }
function abrirModalPartido() { formPartido.value = { codigo: '', nombre: '' }; errorPartido.value = ''; modalPartido.value = true; }
function abrirModalCandidato() { formCandidato.value = { nombre: '', orden_papeleta: 1 }; errorCandidato.value = ''; modalCandidato.value = true; }

async function guardarPartido() {
  errorPartido.value = '';
  try {
    await axios.post('/partidos/', formPartido.value);
    modalPartido.value = false;
    await cargar();
  } catch (e: any) { errorPartido.value = e.response?.data?.detail || 'Error'; }
}

async function guardarCandidato() {
  errorCandidato.value = '';
  try {
    await axios.post('/partidos/candidatos/', { ...formCandidato.value, partido_id: partidoSeleccionado.value!.id });
    modalCandidato.value = false;
    await cargar();
  } catch (e: any) { errorCandidato.value = e.response?.data?.detail || 'Error'; }
}

async function eliminarPartido(id: number) {
  if (!confirm('¿Eliminar partido?')) return;
  try { await axios.delete(`/partidos/${id}`); await cargar(); }
  catch (e: any) { alert(e.response?.data?.detail || 'Error'); }
}

async function eliminarCandidato(id: number) {
  if (!confirm('¿Eliminar candidato?')) return;
  try { await axios.delete(`/partidos/candidatos/${id}`); await cargar(); }
  catch (e: any) { alert(e.response?.data?.detail || 'Error'); }
}

onMounted(cargar);
</script>
