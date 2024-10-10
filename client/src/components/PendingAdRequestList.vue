<script setup>
import { reactive, onMounted } from 'vue';

const state = reactive({
    pending_sent: [],
    pending_received: [],
});

onMounted(async () => {
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
});
</script>

<template>
    <div>
        <h2>Pending Ad Requests</h2>
        <div>
            <h3>Sent</h3>
            <div v-for="ad in state.pending_sent" style="border: 1px solid black;">
                <h4>{{ ad.requirement }}</h4>
                <p>{{ ad.message }}</p>
                <p>Rs. {{ ad.payment_amount }}</p>
                <div>
                    <RouterLink :to="`/ad-request/${ad.id}/edit`">Edit</RouterLink> | 
                    <button @click="deleteAdRequest(ad.id)">Delete</button>
                </div>
            </div>
        </div>
        <div>
            <h3>Received</h3>
            <div v-for="ad in state.pending_received" style="border: 1px solid black;">
                <h4>{{ ad.requirement }}</h4>
                <p>{{ ad.message }}</p>
                <p>Rs. {{ ad.payment_amount }}</p>
                <div>
                    Accept | Reject | Negotiate
                </div>
            </div>
        </div>
    </div>
</template>
