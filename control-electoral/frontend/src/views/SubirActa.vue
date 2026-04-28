<template>
  <div class="p-8 max-w-lg mx-auto">
    <h2 class="text-xl font-bold mb-4">Subir Acta</h2>
    <form @submit.prevent="subirActa" class="space-y-4 bg-white p-6 rounded shadow">

      <label class="block text-sm font-medium">
        Junta
        <select v-model="juntaId" class="input w-full mt-1" required>
          <option value="">Seleccione una junta...</option>
          <option v-for="j in juntas" :key="j.id" :value="j.id">
            {{ j.nombre }} — {{ j.recinto_nombre }}
          </option>
        </select>
      </label>

      <label class="block text-sm font-medium">
        Archivo (JPG, PNG, PDF — máx 10MB)
        <input type="file" @change="onFileChange" accept=".jpg,.jpeg,.png,.pdf" class="input w-full mt-1" required />
      </label>

      <!-- Preview imagen -->
      <div v-if="previewUrl" class="mt-2">
        <img v-if="isImage" :src="previewUrl" class="max-h-48 rounded border" alt="Preview" />
        <p v-else class="text-sm text-gray-600">📄 {{ file?.name }}</p>
      </div>

      <button type="submit" :disabled="enviando" class="btn bg-blue-600 text-white w-full disabled:opacity-50">
        {{ enviando ? 'Subiendo...' : 'Subir Acta' }}
      </button>
      <div v-if="error" class="text-red-600 text-sm">{{ error }}</div>
      <div v-if="url" class="text-green-700 text-sm">✓ Acta subida correctamente</div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';

interface JuntaItem { id: number; nombre: string; recinto_id: number; recinto_nombre: string }

const juntas = ref<JuntaItem[]>([]);
const juntaId = ref<number | ''>('');
const file = ref<File | null>(null);
const previewUrl = ref('');
const error = ref('');
const url = ref('');
const enviando = ref(false);

const isImage = computed(() => file.value?.type.startsWith('image/') ?? false);

onMounted(async () => {
  try {
    const [juntasRes, recintosRes] = await Promise.all([
      axios.get('/juntas/'), axios.get('/recintos/')
    ]);
    const recintoMap: Record<number, string> = {};
    for (const r of recintosRes.data) recintoMap[r.id] = r.nombre;
    juntas.value = juntasRes.data.map((j: any) => ({
      ...j,
      recinto_nombre: recintoMap[j.recinto_id] || `Recinto ${j.recinto_id}`,
    }));
  } catch {
    error.value = 'Error al cargar juntas';
  }
});

function onFileChange(e: Event) {
  const target = e.target as HTMLInputElement;
  file.value = target.files?.[0] || null;
  previewUrl.value = '';
  if (file.value) {
    previewUrl.value = URL.createObjectURL(file.value);
  }
}

async function subirActa() {
  error.value = '';
  url.value = '';
  if (!file.value || !juntaId.value) {
    error.value = 'Debe seleccionar junta y archivo';
    return;
  }
  enviando.value = true;
  const formData = new FormData();
  formData.append('file', file.value);
  try {
    const res = await axios.post(`/upload/acta/${juntaId.value}`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    url.value = res.data.url;
  } catch (e: any) {
    error.value = e.response?.data?.detail || 'Error al subir acta';
  } finally {
    enviando.value = false;
  }
}
</script>
