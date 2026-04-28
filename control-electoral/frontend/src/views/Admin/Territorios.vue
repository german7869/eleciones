<template>
  <div class="p-8 max-w-5xl mx-auto">
    <h2 class="text-xl font-bold mb-4">Gestión Territorial</h2>

    <!-- Tabs -->
    <div class="flex gap-2 mb-6 border-b">
      <button v-for="tab in tabs" :key="tab.key"
        @click="activeTab = tab.key"
        class="px-4 py-2 text-sm font-medium border-b-2 transition-colors"
        :class="activeTab === tab.key ? 'border-blue-600 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700'">
        {{ tab.label }}
      </button>
    </div>

    <!-- Import CSV -->
    <div class="mb-4 p-4 bg-blue-50 rounded border border-blue-200">
      <h3 class="font-bold mb-2 text-blue-900">📊 Importar desde CSV</h3>
      <p class="text-xs text-gray-600 mb-3">
        Importa datos en masse desde archivos CSV. Orden recomendado: 
        <strong>Parroquias → Zonas → Recintos → Juntas</strong>
      </p>
      
      <!-- Botones de ejemplo por tab -->
      <div class="mb-3 pb-3 border-b">
        <div class="text-xs font-semibold text-gray-700 mb-2">Descargar template:</div>
        <div class="flex gap-2 flex-wrap">
          <button v-if="activeTab === 'parroquias'" @click="descargarEjemplo('parroquias_ejemplo.csv')" class="btn bg-gray-600 text-white px-3 py-1 rounded text-xs hover:bg-gray-700">
            📥 parroquias_ejemplo.csv
          </button>
          <button v-else-if="activeTab === 'zonas'" @click="descargarEjemplo('zonas_ejemplo.csv')" class="btn bg-gray-600 text-white px-3 py-1 rounded text-xs hover:bg-gray-700">
            📥 zonas_ejemplo.csv
          </button>
          <button v-else-if="activeTab === 'recintos'" @click="descargarEjemplo('recintos_ejemplo.csv')" class="btn bg-gray-600 text-white px-3 py-1 rounded text-xs hover:bg-gray-700">
            📥 recintos_ejemplo.csv
          </button>
          <button v-else-if="activeTab === 'juntas'" @click="descargarEjemplo('juntas_ejemplo.csv')" class="btn bg-gray-600 text-white px-3 py-1 rounded text-xs hover:bg-gray-700">
            📥 juntas_ejemplo.csv
          </button>
        </div>
      </div>
      
      <!-- Upload section -->
      <div class="space-y-2">
        <div class="flex items-center gap-3 flex-wrap">
          <input type="file" accept=".csv" @change="onCsvChange" class="text-sm" />
          <button @click="importarCSV" :disabled="!csvFile" class="btn bg-green-600 text-white px-4 py-2 rounded text-sm disabled:opacity-50 hover:bg-green-700">
            ✓ Importar CSV
          </button>
        </div>
        <div v-if="csvFile" class="text-xs text-gray-600 bg-white p-2 rounded">
          📄 <strong>{{ csvFile.name }}</strong> ({{ (csvFile.size / 1024).toFixed(2) }} KB)
        </div>
        <div v-if="importMsg" class="text-sm p-3 rounded" :class="importMsg.includes('Error') || importMsg.includes('❌') ? 'bg-red-100 text-red-800 border border-red-300' : 'bg-green-100 text-green-800 border border-green-300'">
          <div class="whitespace-pre-wrap">{{ importMsg }}</div>
        </div>
      </div>
    </div>

    <!-- Parroquias -->
    <div v-if="activeTab === 'parroquias'">
      <div class="flex justify-end mb-2">
        <button @click="abrirModal()" class="btn bg-blue-600 text-white px-3 py-1 rounded text-sm">+ Nueva</button>
      </div>
      <table class="w-full bg-white rounded shadow text-sm">
        <thead class="bg-gray-100"><tr><th class="p-2 text-left">Código</th><th class="p-2 text-left">Nombre</th><th class="p-2 text-right">Votantes</th><th class="p-2"></th></tr></thead>
        <tbody>
          <tr v-for="p in parroquias" :key="p.id" class="border-b">
            <td class="p-2">{{ p.codigo }}</td><td class="p-2">{{ p.nombre }}</td>
            <td class="p-2 text-right">{{ p.nro_votantes }}</td>
            <td class="p-2 flex gap-2">
              <button @click="abrirModal(p)" class="text-blue-600 hover:underline">Editar</button>
              <button @click="eliminar('parroquias', p.id)" class="text-red-500 hover:underline">Eliminar</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Zonas -->
    <div v-if="activeTab === 'zonas'">
      <div class="flex justify-end mb-2">
        <button @click="abrirModal()" class="btn bg-blue-600 text-white px-3 py-1 rounded text-sm">+ Nueva</button>
      </div>
      <table class="w-full bg-white rounded shadow text-sm">
        <thead class="bg-gray-100"><tr><th class="p-2 text-left">Código</th><th class="p-2 text-left">Nombre</th><th class="p-2 text-left">Parroquia</th><th class="p-2"></th></tr></thead>
        <tbody>
          <tr v-for="z in zonas" :key="z.id" class="border-b">
            <td class="p-2">{{ z.codigo }}</td><td class="p-2">{{ z.nombre }}</td>
            <td class="p-2">{{ parroquiaMap[z.parroquia_id] || z.parroquia_id }}</td>
            <td class="p-2 flex gap-2">
              <button @click="abrirModal(z)" class="text-blue-600 hover:underline">Editar</button>
              <button @click="eliminar('zonas', z.id)" class="text-red-500 hover:underline">Eliminar</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Recintos -->
    <div v-if="activeTab === 'recintos'">
      <div class="flex justify-end mb-2">
        <button @click="abrirModal()" class="btn bg-blue-600 text-white px-3 py-1 rounded text-sm">+ Nuevo</button>
      </div>
      <table class="w-full bg-white rounded shadow text-sm">
        <thead class="bg-gray-100"><tr><th class="p-2 text-left">Código</th><th class="p-2 text-left">Nombre</th><th class="p-2 text-left">Zona</th><th class="p-2"></th></tr></thead>
        <tbody>
          <tr v-for="r in recintos" :key="r.id" class="border-b">
            <td class="p-2">{{ r.codigo }}</td><td class="p-2">{{ r.nombre }}</td>
            <td class="p-2">{{ zonaMap[r.zona_id] || r.zona_id }}</td>
            <td class="p-2 flex gap-2">
              <button @click="abrirModal(r)" class="text-blue-600 hover:underline">Editar</button>
              <button @click="eliminar('recintos', r.id)" class="text-red-500 hover:underline">Eliminar</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Juntas -->
    <div v-if="activeTab === 'juntas'">
      <div class="flex justify-end mb-2">
        <button @click="abrirModal()" class="btn bg-blue-600 text-white px-3 py-1 rounded text-sm">+ Nueva</button>
      </div>
      <table class="w-full bg-white rounded shadow text-sm">
        <thead class="bg-gray-100"><tr><th class="p-2 text-left">Código</th><th class="p-2 text-left">Nombre</th><th class="p-2 text-left">Recinto</th><th class="p-2"></th></tr></thead>
        <tbody>
          <tr v-for="ju in juntas" :key="ju.id" class="border-b">
            <td class="p-2">{{ ju.codigo }}</td><td class="p-2">{{ ju.nombre }}</td>
            <td class="p-2">{{ recintosMap[ju.recinto_id] || ju.recinto_id }}</td>
            <td class="p-2 flex gap-2">
              <button @click="abrirModal(ju)" class="text-blue-600 hover:underline">Editar</button>
              <button @click="eliminar('juntas', ju.id)" class="text-red-500 hover:underline">Eliminar</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal genérico -->
    <div v-if="modal" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div class="bg-white rounded shadow-lg p-6 w-full max-w-md">
        <h3 class="font-bold mb-3">{{ editando ? 'Editar' : 'Nuevo' }}</h3>
        <form @submit.prevent="guardar" class="space-y-2">
          <input v-model="form.codigo" placeholder="Código" class="input w-full" required />
          <input v-model="form.nombre" placeholder="Nombre" class="input w-full" required />
          <template v-if="activeTab === 'zonas'">
            <select v-model="form.parroquia_id" class="input w-full" required>
              <option value="">Seleccione parroquia</option>
              <option v-for="p in parroquias" :key="p.id" :value="p.id">{{ p.nombre }}</option>
            </select>
          </template>
          <template v-if="activeTab === 'recintos'">
            <select v-model="form.zona_id" class="input w-full" required>
              <option value="">Seleccione zona</option>
              <option v-for="z in zonas" :key="z.id" :value="z.id">{{ z.nombre }}</option>
            </select>
            <input v-model="form.direccion" placeholder="Dirección (opcional)" class="input w-full" />
          </template>
          <template v-if="activeTab === 'juntas'">
            <select v-model="form.recinto_id" class="input w-full" required>
              <option value="">Seleccione recinto</option>
              <option v-for="r in recintos" :key="r.id" :value="r.id">{{ r.nombre }}</option>
            </select>
          </template>
          <div v-if="modalError" class="text-red-600 text-sm">{{ modalError }}</div>
          <div class="flex gap-2 justify-end">
            <button type="button" @click="modal=false" class="btn border px-3 py-1 rounded">Cancelar</button>
            <button type="submit" class="btn bg-blue-600 text-white px-3 py-1 rounded">Guardar</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import axios from 'axios';

const tabs = [
  { key: 'parroquias', label: 'Parroquias' },
  { key: 'zonas', label: 'Zonas' },
  { key: 'recintos', label: 'Recintos' },
  { key: 'juntas', label: 'Juntas' },
];
const activeTab = ref('parroquias');
const parroquias = ref<any[]>([]);
const zonas = ref<any[]>([]);
const recintos = ref<any[]>([]);
const juntas = ref<any[]>([]);
const modal = ref(false);
const editando = ref<any>(null);
const form = ref<any>({});
const modalError = ref('');
const csvFile = ref<File | null>(null);
const importMsg = ref('');

const parroquiaMap = computed(() => Object.fromEntries(parroquias.value.map(p => [p.id, p.nombre])));
const zonaMap = computed(() => Object.fromEntries(zonas.value.map(z => [z.id, z.nombre])));
const recintosMap = computed(() => Object.fromEntries(recintos.value.map(r => [r.id, r.nombre])));

async function cargar() {
  const [p, z, r, j] = await Promise.all([
    axios.get('/parroquias/'), axios.get('/zonas/'), axios.get('/recintos/'), axios.get('/juntas/')
  ]);
  parroquias.value = p.data; zonas.value = z.data; recintos.value = r.data; juntas.value = j.data;
}

function abrirModal(item?: any) {
  editando.value = item || null;
  modalError.value = '';
  form.value = item ? { ...item } : {};
  modal.value = true;
}

async function guardar() {
  modalError.value = '';
  const url = `/${activeTab.value}/`;
  try {
    if (editando.value) {
      await axios.put(`/${activeTab.value}/${editando.value.id}`, form.value);
    } else {
      await axios.post(url, form.value);
    }
    modal.value = false;
    await cargar();
  } catch (e: any) { modalError.value = e.response?.data?.detail || 'Error'; }
}

async function eliminar(tipo: string, id: number) {
  if (!confirm('¿Eliminar?')) return;
  try { await axios.delete(`/${tipo}/${id}`); await cargar(); }
  catch (e: any) { alert(e.response?.data?.detail || 'Error'); }
}

function onCsvChange(e: Event) {
  const t = e.target as HTMLInputElement;
  csvFile.value = t.files?.[0] || null;
  importMsg.value = '';
}

async function importarCSV() {
  if (!csvFile.value) return;
  importMsg.value = 'Importando...';
  const fd = new FormData();
  fd.append('file', csvFile.value);
  try {
    // Obtener el token del localStorage
    const token = localStorage.getItem('token');
    const res = await axios.post(`/import/${activeTab.value}`, fd, {
      headers: {
        'Content-Type': 'multipart/form-data',
        'Authorization': `Bearer ${token}`
      }
    });
    
    let msg = `✓ Importación completada: ${res.data.insertados} insertados, ${res.data.actualizados} actualizados`;
    
    if (res.data.errores && res.data.errores.length > 0) {
      msg += `\n⚠️ ${res.data.errores.length} error(es): `;
      msg += res.data.errores.slice(0, 3).map((e: any) => `Fila ${e.fila}: ${e.error}`).join('; ');
      if (res.data.errores.length > 3) msg += `... y ${res.data.errores.length - 3} más`;
    }
    
    importMsg.value = msg;
    csvFile.value = null; // Limpiar archivo
    await cargar();
  } catch (e: any) { 
    const detail = e.response?.data?.detail || e.message || 'Error desconocido';
    importMsg.value = `❌ Error: ${detail}`; 
  }
}

function descargarEjemplo(filename: string) {
  // Crear un elemento <a> temporal para descargar
  const link = document.createElement('a');
  // Usar la URL completa del backend
  const baseURL = axios.defaults.baseURL || 'http://localhost:8000';
  link.href = `${baseURL}/ejemplos/${filename}`;
  link.download = filename;
  link.target = '_blank';
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

onMounted(cargar);
</script>
