<script setup>
import Navbar from '@/components/Navbar.vue';
import CampaignForm from '@/components/CampaignForm.vue';
import { onMounted, ref } from 'vue';

const budget = ref(0);

onMounted(async () => {
    try {
        const res = await fetch('/api/sponsor-budget', {
            headers: {
                'Authentication-Token': sessionStorage.getItem('authToken')
            }
        });
        const data = await res.json();
        // console.log(data);
        budget.value = data.budget;
    } catch (error) {
        console.error('Error fetching sponsor budget.', error);
    }
});
</script>

<template>
    <Navbar />
    <CampaignForm title="Edit" :budget="budget" />
</template>
