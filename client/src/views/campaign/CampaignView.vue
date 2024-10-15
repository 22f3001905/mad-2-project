<script setup>
import { ref, onMounted, reactive } from 'vue';
import { useRoute, RouterLink, useRouter } from 'vue-router';

import Navbar from '@/components/Navbar.vue';

const route = useRoute();
const router = useRouter();
const campaignId = ref(route.params.id);
const user = JSON.parse(localStorage.getItem('user'));

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
            headers: { 'Authentication-Token': localStorage.getItem('authToken') }
        });
        router.push('/campaigns');
    } catch (error) {
        console.error('Error in deleting campaign.', error);
    }
}

async function deleteAdRequest(adRequestId) {
    console.log('Ad Request Deleted!');
    try {
        const res = await fetch(`/api/ad-request/${adRequestId}`, {
            method: 'DELETE',
            headers: { 'Authentication-Token': localStorage.getItem('authToken') }
        });
        campaign.adRequests = campaign.adRequests.filter(ad => ad.id != adRequestId);
    } catch (error) {
        console.error('Error in deleting ad request.', error);
    }
}

async function getCampaignInfo(campaign_id) {
    try {
        const res = await fetch(`/api/campaign/${campaignId.value}`, {
            method: 'GET',
            headers: { 'Authentication-Token': localStorage.getItem('authToken') }
        });
        const data = await res.json();
        // console.log(data);
        
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
}

async function acceptAdRequest(adRequestId) {
    // console.log('Ad Request Accepted!');
    try {
        const res = await fetch(`/api/ad-request/${adRequestId}/accept`, {
            method: 'GET',
            headers: { 'Authentication-Token': localStorage.getItem('authToken') }
        });
        const data = await res.json();
        console.log(data);
        await getCampaignInfo();
    } catch (error) {
        console.error('Error in accepting ad request.', error);
    }
}

onMounted(async () => {
    await getCampaignInfo();
});
</script>

<template>
    <Navbar />
    <h1>{{ campaign.name }}</h1>
    <p>{{ campaign.description }}</p>
    <div v-if="user.role == 'Sponsor'">
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
        <p>Influencer: {{ ad.influencer.name || 'Not Assigned' }}</p>

        <div v-if="(user.role == 'Sponsor') && (ad.status != 'Accepted') && (ad.status != 'Completed')">
            <span>Actions: </span>
            <RouterLink :to="(ad.influencer.id > 0 && ad.status == 'Pending') ? `/ad-request/${ad.id}/edit?influencer_id=${ad.influencer.id}` : `/ad-request/${ad.id}/edit`">Edit</RouterLink> |
            <!-- <RouterLink :to="`/ad-request/${ad.id}/edit`">Edit</RouterLink> |  -->
            <button @click="deleteAdRequest(ad.id)">Delete</button>
        </div>

        <div v-if="user.role == 'Influencer' && ad.influencer.id == 0">
            <span>Action: </span>
            <button @click="acceptAdRequest(ad.id)">Accept</button> | 
            <RouterLink :to="`/ad-request/${ad.id}/negotiate`">Negotiate</RouterLink>
        </div>
        
    </div>
    <div v-if="user.role == 'Sponsor'">
        <RouterLink :to="`/ad-request/create?campaign_id=${campaignId}`">
            Create Ad Request <span v-if="campaign.visibility == 'Private'">(Manual Assignment of Ad Request)</span>
        </RouterLink>
        <br>
        <RouterLink to="/search">Search for Influencers</RouterLink>
    </div>
</template>
