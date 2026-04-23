<template>
  <div class="p-8 max-w-lg mx-auto">
    <h2 class="text-xl font-bold mb-4">Subir Acta</h2>
    <form @submit.prevent="subirActa" class="space-y-4 bg-white p-6 rounded shadow">
      <label class="block">
        ID de Junta:
        <input v-model="juntaId" type="number" class="input w-full mt-1" required />
      </label>
      <label class="block">
        Archivo (JPG, PNG, PDF, máx 10MB):
        <input type="file" @change="onFileChange" accept=".jpg,.jpeg,.png,.pdf" class="input w-full mt-1" required />
      </label>
      <button type="submit" class="btn bg-blue-600 text-white w-full">Subir</button>
      <div v-if="error" class="text-red-600 mt-2">{{ error }}</div>
      <div v-if="url" class="text-green-700 mt-2">Archivo subido: {{ url }}</div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios';

const juntaId = ref('');
const file = ref<File|null>(null);
const error = ref('');
const url = ref('');

function onFileChange(e: Event) {
  const target = e.target as HTMLInputElement;
  file.value = target.files && target.files[0] ? target.files[0] : null;
}

async function subirActa() {
  error.value = '';
  url.value = '';
  if (!file.value || !juntaId.value) {
    error.value = 'Debe seleccionar archivo y junta';
    return;
  }
  const formData = new FormData();
  formData.append('file', file.value);
  try {
    const res = await axios.post(`/upload/acta/${juntaId.value}`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    url.value = res.data.url;
  } catch (e: any) {
    error.value = e.response?.data?.detail || 'Error al subir acta';
  }
}
</script>
