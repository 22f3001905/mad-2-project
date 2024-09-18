<script setup>
import { ref, onMounted, reactive } from 'vue';
import { useRoute, RouterLink } from 'vue-router';

import Navbar from '@/components/Navbar.vue';

const route = useRoute();
const campaignId = ref(route.params.id);

const campaign = reactive({
    id: null,
    name: '',
    description: '',
    startDate: '',
    endDate: '',
    budget: null,
    niche: '',
    visibility: ''
});

onMounted(async () => {
    try {
        const res = await fetch(`/api/campaign/${campaignId.value}`, {
            headers: { 'Authentication-Token': sessionStorage.getItem('authToken') }
        });
        const data = await res.json();
        console.log(data);
        
        campaign.id = data.id;
        campaign.name = data.name;
        campaign.description = data.description;
        campaign.startDate = data.start_date;
        campaign.endDate = data.end_date;
        campaign.budget = data.budget;
        campaign.niche = data.niche;
        campaign.visibility = data.visibility;
    } catch (error) {
        console.error('Error in fetching campaign data.', error);
    }
});
</script>

<template>
    <Navbar />
    <h1>{{ campaign.name }}</h1>
    <p>{{ campaign.description }}</p>
    <div>
        <RouterLink to="/campaign/create">Create a New Campaign</RouterLink>
    </div>
</template>
