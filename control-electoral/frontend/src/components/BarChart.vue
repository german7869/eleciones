<template>
  <canvas ref="canvas"></canvas>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
let chart: any = null;
const props = defineProps<{ labels: string[]; data: number[] }>();
const canvas = ref<HTMLCanvasElement|null>(null);

onMounted(async () => {
  if (!canvas.value) return;
  const Chart = (await import('chart.js/auto')).default;
  chart = new Chart(canvas.value, {
    type: 'bar',
    data: {
      labels: props.labels,
      datasets: [{ label: 'Votos', data: props.data, backgroundColor: '#2563eb' }]
    },
    options: { responsive: true, plugins: { legend: { display: false } } }
  });
});

watch(() => [props.labels, props.data], ([labels, data]) => {
  if (chart) {
    chart.data.labels = labels;
    chart.data.datasets[0].data = data;
    chart.update();
  }
});
</script>
