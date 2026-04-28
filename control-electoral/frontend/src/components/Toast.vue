<template>
  <div class="fixed bottom-4 right-4 flex flex-col gap-2 z-50">
    <transition-group name="toast">
      <div
        v-for="t in toasts"
        :key="t.id"
        class="px-4 py-3 rounded shadow-lg text-white text-sm max-w-xs"
        :class="{
          'bg-green-600': t.type === 'success',
          'bg-red-600': t.type === 'error',
          'bg-blue-600': t.type === 'info',
          'bg-yellow-600': t.type === 'warning',
        }"
      >
        {{ t.message }}
      </div>
    </transition-group>
  </div>
</template>

<script setup lang="ts">
import { useToast } from '../composables/useToast';
const { toasts } = useToast();
</script>

<style scoped>
.toast-enter-active, .toast-leave-active { transition: all 0.3s ease; }
.toast-enter-from, .toast-leave-to { opacity: 0; transform: translateX(100%); }
</style>
