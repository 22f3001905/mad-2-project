<script setup>
import Navbar from '@/components/Navbar.vue';
import { reactive, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const state = reactive({
    walletBalance: null,
    assignedAds: []
})

const getInfluencerInfo = async () => {
    try {
        const res = await fetch('/api/info/influencer', {
            method: 'GET',
            headers: { 'Authentication-Token': localStorage.getItem('authToken') }
        });
        const data = await res.json();
        console.log(data);
        state.walletBalance = data.wallet_balance;
        state.assignedAds = [...data.assigned_ads];
    } catch (error) {
        console.error('Error fetching influencer info.', error);
    }
}

async function acceptAdRequest(adRequestId) {
    try {
        const res = await fetch(`/api/ad-request/${adRequestId}/accept`, {
            method: 'GET',
            headers: { 'Authentication-Token': localStorage.getItem('authToken') }
        });
        const data = await res.json();
        // console.log(data);
        await getInfluencerInfo();
    } catch (error) {
        console.error('Error in accepting ad request.', error);
    }
}

async function rejectAdRequest(adRequestId) {
    console.log('Ad Request Accepted!');
    try {
        const res = await fetch(`/api/ad-request/${adRequestId}/reject`, {
            method: 'GET',
            headers: { 'Authentication-Token': localStorage.getItem('authToken') }
        });
        const data = await res.json();
        console.log(data);
        await getInfluencerInfo();
    } catch (error) {
        console.error('Error in accepting ad request.', error);
    }
}

async function completeAdRequest(adRequestId) {
    console.log(adRequestId, 'is completed.');
    try {
        const res = await fetch(`/api/ad-request/${adRequestId}/complete`, {
            method: 'GET',
            headers: { 'Authentication-Token': localStorage.getItem('authToken') }
        });
        const data = await res.json();
        // console.log(data);
        await getInfluencerInfo();
    } catch (error) {
        console.error('Error in accepting ad request.', error);
    }
}

onMounted(async () => {
    await getInfluencerInfo();
})
</script>

<template>
    <Navbar />
    <h2>Adverts</h2>
    <div>
        <p>Wallet: Rs. {{ state.walletBalance }}</p>
    </div>
    <div>
        <div v-for="ad in state.assignedAds" style="border: 1px solid black;">
            <h3>{{ ad.requirement }}</h3>
            <p>Status: {{ ad.status }} | Payment: Rs. {{ ad.payment_amount }}</p>
            <p>{{ ad.message }}</p>
            <div v-if="ad.status != 'Completed' && ad.status != 'Rejected'">
                <span>Actions: </span>
                <span v-if="ad.status == 'Pending'">
                    <button @click="acceptAdRequest(ad.id)">Accept</button> | 
                    <button @click="rejectAdRequest(ad.id)">Reject</button> |
                    <RouterLink :to="`/ad-request/${ad.id}/negotiate`">Negotiate</RouterLink>
                </span>
                <span v-else>
                    <button @click="completeAdRequest(ad.id)">Complete</button>
                </span>
            </div>
        </div>
    </div>
</template>
