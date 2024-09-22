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

async function deleteCampaign() {
    console.log('Campaign Deleted!');
    try {
        const res = await fetch(`/api/campaign/${campaignId.value}`, {
            method: 'DELETE',
            headers: { 'Authentication-Token': sessionStorage.getItem('authToken') }
        });
        router.push('/campaigns')
    } catch (error) {
        console.error('Error in deleting campaign.', error);
    }
}

onMounted(async () => {
    try {
        const res = await fetch(`/api/campaign/${campaignId.value}`, {
            method: 'GET',
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
        campaign.niche = data.niche.name;
        campaign.visibility = data.visibility.name;
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
        <span>Actions: </span>
        <RouterLink :to="`/campaign/${campaignId}/edit`">Edit</RouterLink>
        <button @click="deleteCampaign">Delete</button>
    </div>
</template>
