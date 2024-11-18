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
    <div class="container my-4">
        <h2 class="mb-4">Active Campaigns</h2>
        <div class="row">
            <div 
                v-for="campaign in state.activeCampaigns" 
                :key="campaign.id" 
                class="col-md-6 mb-4"
            >
                <div class="card shadow-sm h-100">
                    <div class="card-body d-flex flex-column">
                        <h3 class="card-title">{{ campaign.name }}</h3>

                        <ul class="list-unstyled">
                            <li>
                                <strong>Ends:</strong> {{ new Date(campaign.end_date).toDateString() }}
                            </li>
                            <li>
                                <strong>Visibility:</strong> {{ campaign.visibility }}
                            </li>
                            <li v-if="campaign.flagged" class="badge bg-danger">
                                Flagged
                            </li>
                        </ul>

                        <div class="d-flex gap-2 mt-auto">
                            <RouterLink 
                                :to="`/campaign/${campaign.id}`" 
                                class="btn btn-primary btn-sm"
                            >
                                View
                            </RouterLink>
                            <button 
                                v-if="props.role == 'Admin'" 
                                class="btn btn-warning btn-sm"
                                @click="!campaign.flagged ? flagCampaign(campaign.id) : unflagCampaign(campaign.id)"
                            >
                                {{ !campaign.flagged ? 'Flag' : 'Unflag' }}
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="row" v-if="state.activeCampaigns.length == 0">
            <p class="text-muted">
                No active campaigns.
            </p>
        </div>
    </div>
</template>
