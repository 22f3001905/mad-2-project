<script setup>
import Chart from '@/components/stats/Chart.vue';
import { onMounted, reactive } from 'vue';

const zip = (a, b) => a.map((k, i) => [k, b[i]]);

onMounted(async () => {
    try {
        const res = await fetch('/api/sponsor/stats', {
            headers: {
                'Authentication-Token': localStorage.getItem('authToken')
            }
        });
        const data = await res.json();
        console.log(data);
    } catch (error) {
        console.error('Error fetching charts data.', error);
    }
});
</script>

<template>
    <div>
        <h1>Sponsor Statistics</h1>
    </div>
</template>
