<script setup>
import { defineProps, ref, reactive, onMounted } from 'vue';

const props = defineProps({
    role: String
});

const state = reactive({
    activeCampaigns: [],
});

onMounted(async () => {
    try {
        const res = await fetch('/api/active-campaigns', {
            method: 'GET',
            headers: { 'Authentication-Token': localStorage.getItem('authToken') }
        });
        const data = await res.json();
        console.log(data);
        state.activeCampaigns = [...data.campaigns];
    } catch (error) {
        console.error('Error fetching active campaigns', error);
    }
});
</script>

<template>
    <div>
        <h2>Active Campaigns</h2>
        <div>
            <div v-for="campaign in state.activeCampaigns" style="border: 1px solid black;">
                <h3>{{ campaign.name }}</h3>
                <p>Ends: {{ new Date(campaign.end_date).toDateString() }}</p>
                <p>{{ campaign.visibility }}</p>
                <p v-if="campaign.flagged">Flagged!</p>
                <div>
                    <RouterLink :to="`/campaign/${campaign.id}`">View</RouterLink>
                </div>
            </div>
        </div>
    </div>
</template>
