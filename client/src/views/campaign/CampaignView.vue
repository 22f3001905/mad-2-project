<script setup>
import { ref, onMounted, reactive } from 'vue';
import { useRoute, RouterLink, useRouter } from 'vue-router';

import Navbar from '@/components/Navbar.vue';

const route = useRoute();
const router = useRouter();
const campaignId = ref(route.params.id);

const campaign = reactive({
    id: null,
    name: '',
    description: '',
    startDate: '',
    endDate: '',
    budget: null,
    niche: '',
    visibility: '',
    adRequests: []
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
        campaign.adRequests = data.ad_requests;
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
        <RouterLink :to="`/campaign/${campaignId}/edit`">Edit</RouterLink> |
        <button @click="deleteCampaign">Delete</button>
    </div>
    <h2>Campaign Info</h2>
    <div>
        <p>Budget: Rs. {{ campaign.budget }}</p>
        <p>{{ campaign.startDate }} to {{ campaign.endDate }}</p>
        <p>{{ campaign.niche }} | {{ campaign.visibility }}</p>
    </div>
    <h2>Ad Requests</h2>
    <div v-for="ad in campaign.adRequests" style="border: 1px solid black;">
        <h3>{{ ad.requirement }}</h3>
        <p>Status: {{ ad.status }} | Payment: Rs. {{ ad.payment_amount }}</p>
        <p>{{ ad.message }}</p>
        <div v-if="ad.status != 'Accepted'">
            <span>Actions: </span>
            <RouterLink :to="`/ad-request/${ad.id}/edit`">Edit</RouterLink> |
            <button @click="deleteAdRequest">Delete</button>
        </div>
        <div v-else>
            <p>Influencer: {{ ad.influencer }}</p>
        </div>
    </div>
    <div>
        <RouterLink to="/ad-request/create">Create Ad</RouterLink>
    </div>
</template>
