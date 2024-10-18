<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);

const props = defineProps({
    chartType: {
        type: String,
        required: true,
    },
    chartData: {
        type: Object,
        required: true,
    },
    chartOptions: {
        type: Object,
        required: false,
    },
});

const chartCanvas = ref(null);
let chart = null;

onMounted(() => {
    chart = new Chart(chartCanvas.value, {
        type: props.chartType,
        data: props.chartData,
        options: props.chartOptions,
    });
});

onBeforeUnmount(() => {
    if (chart) {
        chart.destroy();
    }
});
</script>

<template>
    <div>
        <canvas ref="chartCanvas"></canvas>
    </div>
</template>

<style scoped>
/* canvas {
    max-width: 600px;
    max-height: 400px;
} */
</style>
