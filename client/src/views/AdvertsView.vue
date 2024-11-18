<script setup>
import Navbar from '@/components/Navbar.vue';
import { reactive, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { formatNumber } from '@/utils';

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
    <h2 class="pt-4 mb-3">Adverts List</h2>
    
    <div class="mb-4 p-3 border rounded shadow-sm alert alert-primary">
        <strong>Wallet Balance:</strong> Rs. {{ formatNumber(state.walletBalance) }}
    </div>
    
    <div class="row">
        <div 
            v-for="ad in state.assignedAds" 
            :key="ad.id" 
            class="col-md-6 mb-4" 
        >
            <div class="card shadow-sm h-100">
                <div class="card-body d-flex flex-column">
                    <h3 class="card-title">{{ ad.requirement }}</h3>
                    <p class="card-text">{{ ad.message }}</p>

                    <ul class="list-unstyled">
                        <li>
                            <strong>Campaign:</strong> <RouterLink :to="`/campaign/${ad.campaign.id}`">{{ ad.campaign.name }}</RouterLink>
                        </li>
                        <li>
                            <strong>Status:</strong> {{ ad.status }}
                        </li>
                        <li>
                            <strong>Payout:</strong> Rs. {{ formatNumber(ad.payment_amount) }}
                        </li>
                    </ul>

                    <div 
                        v-if="(ad.status != 'Completed') && (ad.status != 'Rejected')" 
                        class="mt-auto"
                    >
                        <!-- Pending to Accept -->
                        <div 
                            v-if="ad.status == 'Pending'" 
                            class="d-flex gap-2"
                        >
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
                        <!-- Accepted On-going Action -->
                        <div v-else>
                            <button 
                                @click="completeAdRequest(ad.id)" 
                                class="btn btn-dark btn-sm"
                            >
                                Complete
                            </button>
                        </div>
                    </div>
                    <div v-else-if="ad.status == 'Completed'">
                        <button class="btn btn-light btn-sm" disabled>
                            Ad request has been completed
                        </button>
                    </div>
                    <div v-else>
                        <button class="btn btn-light btn-sm" disabled>
                            Ad request has been rejected
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="text-center mt-4">
        <RouterLink to="/search" class="btn btn-outline-primary">
            Search For Campaigns
        </RouterLink>
    </div>
</template>
