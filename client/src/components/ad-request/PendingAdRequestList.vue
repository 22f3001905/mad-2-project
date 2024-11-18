<script setup>
import { reactive, onMounted, computed } from 'vue';
import { useUserStore } from '@/stores/user';
import { formatNumber } from '@/utils';

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
    <div class="my-4">
        <h2 class="mb-3">Pending Ad Requests</h2>
        <p class="text-muted">These are the pending ad requests that require user action.</p>

        <!-- Sent Ad Requests -->
        <div class="mb-4">
            <h3 class="mb-2">Sent</h3>
            <p class="text-muted">Wait for the ad request to be accepted or modify it.</p>
            <div class="row">
                <div 
                    v-for="ad in state.pending_sent" 
                    :key="ad.id" 
                    class="col-md-6 mb-3"
                >
                    <div class="card shadow-sm h-100">
                        <div class="card-body d-flex flex-column">
                            <h4 class="card-title">{{ ad.requirement }}</h4>
                            <p class="card-text">{{ ad.message }}</p>

                            <ul class="list-unstyled">
                                <li v-if="userRole == 'Sponsor'">
                                    <strong>Influencer:</strong> {{ ad.influencer_name }}
                                </li>
                                <li v-else>
                                    <strong>Sponsor:</strong> {{ ad.sponsor_name }}
                                </li>
                                <li>
                                    <strong>Payout:</strong> Rs. {{ formatNumber(ad.payment_amount) }}
                                </li>
                            </ul>

                            <div class="d-flex gap-2 mt-auto">
                                <RouterLink 
                                    :to="`/ad-request/${ad.id}/edit`" 
                                    class="btn btn-warning btn-sm"
                                >
                                    Edit
                                </RouterLink>
                                <button 
                                    @click="deleteAdRequest(ad.id)" 
                                    class="btn btn-danger btn-sm"
                                >
                                    Delete
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
                <div v-if="state.pending_sent.length == 0">
                    <p class="mb-0">No ad requests sent.</p>
                </div>
            </div>
        </div>

        <!-- Received Ad Requests -->
        <div>
            <h3 class="mb-2">Received</h3>
            <p class="text-muted">Accept, reject, or negotiate a better payout for these ad requests.</p>
            <div class="row">
                <div 
                    v-for="ad in state.pending_received" 
                    :key="ad.id" 
                    class="col-md-6 mb-3"
                >
                    <div class="card shadow-sm h-100">
                        <div class="card-body d-flex flex-column">
                            <h4 class="card-title">{{ ad.requirement }}</h4>
                            <p class="card-text">{{ ad.message }}</p>

                            <ul class="list-unstyled">
                                <li v-if="userRole == 'Sponsor'">
                                    <strong>Influencer:</strong> {{ ad.influencer_name }}
                                </li>
                                <li v-else>
                                    <strong>Sponsor:</strong> {{ ad.sponsor_name }}
                                </li>
                                <li>
                                    <strong>Payout:</strong> Rs. {{ formatNumber(ad.payment_amount) }}
                                </li>
                            </ul>

                            <div class="d-flex gap-2 mt-auto">
                                <button 
                                    @click="acceptAdRequest(ad.id)" 
                                    class="btn btn-success btn-sm"
                                >
                                    Accept
                                </button>
                                <button 
                                    @click="rejectAdRequest(ad.id)" 
                                    class="btn btn-danger btn-sm"
                                >
                                    Reject
                                </button>
                                <RouterLink 
                                    :to="`/ad-request/${ad.id}/negotiate`" 
                                    class="btn btn-warning btn-sm"
                                >
                                    Negotiate
                                </RouterLink>
                            </div>
                        </div>
                    </div>
                </div>
                <div v-if="state.pending_received.length == 0">
                    <p class="mb-0">No ad requests received.</p>
                </div>
            </div>
        </div>
    </div>
</template>
