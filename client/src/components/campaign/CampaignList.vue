<script setup>
import { reactive, onMounted } from 'vue';
import { RouterLink } from 'vue-router';

import DownloadCampaignData from '@/components/campaign/DownloadCampaignData.vue';

const state = reactive({
    campaigns: []
});
const user = JSON.parse(localStorage.getItem('user'));

onMounted(async () => {
    try {
        const res = await fetch(`/api/${user.role == 'Sponsor' ? 'sponsor' : 'influencer'}/campaigns`, {
            method: 'GET',
            headers: { 'Authentication-Token': localStorage.getItem('authToken') }
        });
        const data = await res.json();
        console.log(data.campaigns);
        state.campaigns = [...data.campaigns];  // creates a copy
    } catch (error) {
        console.error('Error fetching all the campaigns for this user.', error);
    }
});
</script>

<template>
    <!-- <section class="container my-4">
        <h2 class="mb-3">
            {{ user.role == 'Influencer' ? 'Public' : '' }} Campaign List
        </h2>
        <DownloadCampaignData />
        <div>
            <div v-for="campaign in state.campaigns" style="border: 1px solid black;">
                <h3>{{ campaign.name }}</h3>
                <p>{{ campaign.description }}</p>
                <p>Starts: {{ new Date(campaign.start_date).toDateString() }} | Ends: {{ new Date(campaign.end_date).toDateString() }}</p>
                <p>{{ campaign.visibility }}</p>
                <p>Budget: Rs. {{ campaign.budget }}</p>
                <p>Niche: {{ campaign.niche }}</p>
                <div>
                    <RouterLink :to="`/campaign/${campaign.id}`">View</RouterLink>
                </div>
            </div>
        </div>
    </section> -->
    <section class="container my-4">
        <h2 class="mb-3">
            {{ user.role == 'Influencer' ? 'Public' : '' }} Campaign List
        </h2>
        <!-- Download Button Component -->
        <div class="mb-4">
            <DownloadCampaignData />
        </div>

        <!-- Campaign List -->
        <div class="row">
            <div 
                v-for="campaign in state.campaigns" 
                :key="campaign.id" 
                class="col-md-6 col-lg-4 mb-4"
            >
                <div class="card shadow-sm h-100">
                    <div class="card-body d-flex flex-column">
                        <h3 class="card-title">{{ campaign.name }}</h3>
                        <p class="card-text text-muted">{{ campaign.description }}</p>
                        
                        <ul class="list-unstyled">
                            <li>
                                <strong>Starts:</strong> {{ new Date(campaign.start_date).toDateString() }}
                            </li>
                            <li>
                                <strong>Ends:</strong> {{ new Date(campaign.end_date).toDateString() }}
                            </li>
                        </ul>

                        <ul class="list-unstyled">
                            <li>
                                <strong>Visibility:</strong> {{ campaign.visibility }}
                            </li>
                            <li>
                                <strong>Budget:</strong> Rs. {{ campaign.budget }}
                            </li>
                            <li>
                                <strong>Niche:</strong> {{ campaign.niche }}
                            </li>
                        </ul>
                        <div class="mt-auto">
                            <RouterLink 
                                :to="`/campaign/${campaign.id}`" 
                                class="btn btn-primary btn-sm"
                            >
                                View
                            </RouterLink>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="row" v-if="state.campaigns.length == 0">
            <p class="text-muted">
                No campaigns created yet.
            </p>
        </div>
    </section>
</template>
