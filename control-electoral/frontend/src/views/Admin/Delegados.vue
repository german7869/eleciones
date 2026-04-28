<template>
  <div class="p-8 max-w-4xl mx-auto">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-xl font-bold">Gestión de Delegados</h2>
      <button @click="abrirModal()" class="btn bg-blue-600 text-white px-4 py-2 rounded">+ Nuevo</button>
    </div>

    <table class="min-w-full bg-white rounded shadow">
      <thead class="bg-gray-100">
        <tr>
          <th class="p-2 text-left">Nombre</th>
          <th class="p-2 text-left">Cédula</th>
          <th class="p-2 text-left">Teléfono</th>
          <th class="p-2 text-left">Rol</th>
          <th class="p-2"></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="d in delegados" :key="d.id" class="border-b">
          <td class="p-2">{{ d.nombre }}</td>
          <td class="p-2">{{ d.cedula }}</td>
          <td class="p-2">{{ d.telefono || '—' }}</td>
          <td class="p-2"><span :class="d.rol === 'admin' ? 'text-blue-600 font-bold' : 'text-gray-500'">{{ d.rol }}</span></td>
          <td class="p-2 flex gap-2">
            <button @click="abrirModal(d)" class="text-blue-600 hover:underline text-sm">Editar</button>
            <button @click="eliminar(d.id)" class="text-red-600 hover:underline text-sm">Eliminar</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Modal -->
    <div v-if="modal" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div class="bg-white rounded shadow-lg p-6 w-full max-w-md">
        <h3 class="font-bold text-lg mb-4">{{ editando ? 'Editar' : 'Nuevo' }} Delegado</h3>
        <form @submit.prevent="guardar" class="space-y-3">
          <input v-model="form.nombre" placeholder="Nombre" class="input w-full" required />
          <input v-model="form.cedula" placeholder="Cédula" class="input w-full" required />
          <input v-model="form.telefono" placeholder="Teléfono (opcional)" class="input w-full" />
          <input v-model="form.password" type="password" placeholder="Contraseña" class="input w-full" :required="!editando" />
          <select v-model="form.rol" class="input w-full">
            <option value="delegado">delegado</option>
            <option value="admin">admin</option>
          </select>
          <div v-if="error" class="text-red-600 text-sm">{{ error }}</div>
          <div class="flex gap-2 justify-end">
            <button type="button" @click="modal = false" class="btn px-4 py-2 border rounded">Cancelar</button>
            <button type="submit" class="btn bg-blue-600 text-white px-4 py-2 rounded">Guardar</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';

interface Delegado { id: number; nombre: string; cedula: string; telefono: string; rol: string }

const delegados = ref<Delegado[]>([]);
const modal = ref(false);
const editando = ref<Delegado | null>(null);
const error = ref('');
const form = ref({ nombre: '', cedula: '', telefono: '', password: '', rol: 'delegado' });

async function cargar() {
  delegados.value = (await axios.get('/delegados/')).data;
}

function abrirModal(d?: Delegado) {
  editando.value = d || null;
  error.value = '';
  form.value = d
    ? { nombre: d.nombre, cedula: d.cedula, telefono: d.telefono || '', password: '', rol: d.rol }
    : { nombre: '', cedula: '', telefono: '', password: '', rol: 'delegado' };
  modal.value = true;
}

async function guardar() {
  error.value = '';
  try {
    if (editando.value) {
      await axios.put(`/delegados/${editando.value.id}`, form.value);
    } else {
      await axios.post('/delegados/', form.value);
    }
    modal.value = false;
    await cargar();
  } catch (e: any) {
    error.value = e.response?.data?.detail || 'Error al guardar';
  }
}

async function eliminar(id: number) {
  if (!confirm('¿Eliminar este delegado?')) return;
  try {
    await axios.delete(`/delegados/${id}`);
    await cargar();
  } catch (e: any) {
    alert(e.response?.data?.detail || 'Error al eliminar');
  }
}

onMounted(cargar);
</script>
