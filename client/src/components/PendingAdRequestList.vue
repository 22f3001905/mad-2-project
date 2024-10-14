<script setup>
import { reactive, onMounted, computed } from 'vue';
import { useUserStore } from '@/stores/user';

const store = useUserStore();
const userRole = computed(() => store.getUserRole);

const state = reactive({
    pending_sent: [],
    pending_received: [],
});

async function acceptAdRequest(adRequestId) {
    console.log('Ad Request Accepted!');
    try {
        const res = await fetch(`/api/ad-request/${adRequestId}/accept`, {
            method: 'GET',
            headers: { 'Authentication-Token': localStorage.getItem('authToken') }
        });
        const data = await res.json();
        console.log(data);
        await getPendingAdRequests();
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
        await getPendingAdRequests();
    } catch (error) {
        console.error('Error in accepting ad request.', error);
    }
}

async function getPendingAdRequests() {
    try {
        const res = await fetch('/api/pending-ad-requests', {
            method: 'GET',
            headers: { 'Authentication-Token': localStorage.getItem('authToken') }
        });
        const data = await res.json();
        console.log(data);
        state.pending_sent = [...data.pending_ad_requests.sent]
        state.pending_received = [...data.pending_ad_requests.received]
    } catch (error) {
        console.error('Error fetching active campaigns', error);
    }
}

const deleteAdRequest = async () => {
    console.log('delete ad request.')
}

onMounted(async () => {
    await getPendingAdRequests();
});
</script>

<template>
    <div>
        <h2>Pending Ad Requests</h2>
        <p>These are the pending ad requests that require user action.</p>
        <div>
            <h3>Sent</h3>
            <p>Wait for the ad request to be accepted or modify it.</p>
            <div v-for="ad in state.pending_sent" style="border: 1px solid black;">
                <h4>{{ ad.requirement }}</h4>
                <p>{{ ad.message }}</p>
                <p v-if="userRole == 'Sponsor'">Influencer: {{ ad.influencer_name }}</p>
                <p v-else>Sponsor: {{ ad.sponsor_name }}</p>
                <p>Payout: Rs. {{ ad.payment_amount }}</p>
                <div>
                    <RouterLink :to="`/ad-request/${ad.id}/edit`">Edit</RouterLink> | 
                    <button @click="deleteAdRequest(ad.id)">Delete</button>
                </div>
            </div>
        </div>
        <div>
            <h3>Received</h3>
            <p>Accept, reject, or negotiate a better payout for these ad request.</p>
            <div v-for="ad in state.pending_received" style="border: 1px solid black;">
                <h4>{{ ad.requirement }}</h4>
                <p>{{ ad.message }}</p>
                <p v-if="userRole == 'Sponsor'">Influencer: {{ ad.influencer_name }}</p>
                <p v-else>Sponsor: {{ ad.sponsor_name }}</p>
                <p>Payout: Rs. {{ ad.payment_amount }}</p>
                <div>
                    <span>Action: </span>
                    <button @click="acceptAdRequest(ad.id)">Accept</button> | 
                    <button @click="rejectAdRequest(ad.id)">Reject</button> | 
                    <RouterLink :to="`/ad-request/${ad.id}/negotiate`">Negotiate</RouterLink>
                </div>
            </div>
        </div>
    </div>
</template>
