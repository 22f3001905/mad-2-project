<script setup>
import { defineProps, ref, reactive, onMounted } from 'vue';

const props = defineProps({
    role: { type: String, required: true }
});

const state = reactive({
    activeCampaigns: [],
});

const flagCampaign = async (campaignId) => {
    try {
        const res = await fetch(`/api/campaign/${campaignId}/flag`, {
            method: 'GET',
            headers: { 'Authentication-Token': localStorage.getItem('authToken') }
        });
        const data = await res.json();
        console.log(data);
        state.activeCampaigns.filter(camp => camp.id == campaignId)[0].flagged = true;
    } catch (error) {
        console.error('Error in flagging campaign.', error);
    }
}

const unflagCampaign = async (campaignId) => {
    try {
        const res = await fetch(`/api/campaign/${campaignId}/unflag`, {
            method: 'GET',
            headers: { 'Authentication-Token': localStorage.getItem('authToken') }
        });
        const data = await res.json();
        console.log(data);
        state.activeCampaigns.filter(camp => camp.id == campaignId)[0].flagged = false;
    } catch (error) {
        console.error('Error in unflagging campaign.', error);
    }
}

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
                <p v-if="campaign.flagged">Flagged! TODO: Color red!</p>
                <div>
                    <RouterLink :to="`/campaign/${campaign.id}`">View</RouterLink>
                    <button 
                        v-if="props.role == 'Admin'" 
                        @click="!campaign.flagged ? flagCampaign(campaign.id) : unflagCampaign(campaign.id)"
                    >
                        {{ !campaign.flagged ? 'Flag' : 'Unflag' }}
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>
