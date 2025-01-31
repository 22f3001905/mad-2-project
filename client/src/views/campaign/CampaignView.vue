<script setup>
import { ref, onMounted, reactive, computed } from 'vue';
import { useRoute, RouterLink, useRouter } from 'vue-router';
import { formatNumber, redirectToErrorPage } from '@/utils';
import { useUserStore } from '@/stores/user';

const store = useUserStore();
const userId = computed(() => store.getUserId);

// console.log("USER ID:", userId.value);

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

const state = reactive({
    influencerId: null,
});

async function deleteCampaign() {
    console.log('Campaign Deleted!');
    try {
        const confirmDelete = window.confirm("Are you sure you want to delete this campaign?");
        if (!confirmDelete) {
            return null;
        }

        const res = await fetch(`/api/campaign/${campaignId.value}`, {
            method: 'DELETE',
            headers: { 'Authentication-Token': localStorage.getItem('authToken') }
        });

        if (!res.ok) {
            return redirectToErrorPage(res.status, router);
        }

        return router.push('/campaigns');
    } catch (error) {
        console.error('Error in deleting campaign.', error);
    }
}

async function deleteAdRequest(adRequestId) {
    console.log('Ad Request Deleted!');
    try {
        const confirmDelete = window.confirm("Are you sure you want to delete this ad request?");
        if (!confirmDelete) {
            return null;
        }

        const res = await fetch(`/api/ad-request/${adRequestId}`, {
            method: 'DELETE',
            headers: { 'Authentication-Token': localStorage.getItem('authToken') }
        });

        if (!res.ok) {
            return redirectToErrorPage(res.status, router);
        }

        campaign.budget += campaign.adRequests.filter(ad => ad.id == adRequestId)[0].payment_amount;
        campaign.adRequests = campaign.adRequests.filter(ad => ad.id != adRequestId);
    } catch (error) {
        console.error('Error in deleting ad request.', error);
    }
}

async function getCampaignInfo() {
    try {
        const res = await fetch(`/api/campaign/${campaignId.value}`, {
            method: 'GET',
            headers: { 'Authentication-Token': localStorage.getItem('authToken') }
        });

        if (!res.ok) {
            return redirectToErrorPage(res.status, router);
        }
        
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
        campaign.adRequests = data.ad_requests.toReversed();
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

        if (!res.ok) {
            return redirectToErrorPage(res.status, router);
        }

        const data = await res.json();
        console.log(data);
        await getCampaignInfo();
    } catch (error) {
        console.error('Error in accepting ad request.', error);
    }
}

async function fetchInfluencerInfo() {
    try {
        const res = await fetch('/api/info/influencer', {
            method: 'GET',
            headers: { 'Authentication-Token': localStorage.getItem('authToken') }
        });

        if (!res.ok) {
            return redirectToErrorPage(res.status, router);
        }

        const data = await res.json();
        console.log(data);
        state.influencerId = data.id;
    } catch (error) {
        console.error('Error in fetching influencer info.', error);
    }
}

async function rejectAdRequest(adRequestId) {
    console.log('Ad Request rejected!');
    try {
        const confirmReject = window.confirm("Are you sure you want to reject this ad request?");
        if (!confirmReject) {
            return null;
        }
        
        const res = await fetch(`/api/ad-request/${adRequestId}/reject`, {
            method: 'GET',
            headers: { 'Authentication-Token': localStorage.getItem('authToken') }
        });

        if (!res.ok) {
            return redirectToErrorPage(res.status, router);
        }

        const data = await res.json();
        console.log(data);
        await getCampaignInfo();
    } catch (error) {
        console.error('Error in accepting ad request.', error);
    }
}

async function unassignAdRequests(adRequestId) {
    console.log('Ad request is unassigned');
    try {
        const res = await fetch(`/api/ad-request/${adRequestId}/unassign`, {
            method: 'GET',
            headers: { 'Authentication-Token': localStorage.getItem('authToken') }
        });

        if (!res.ok) {
            return redirectToErrorPage(res.status, router);
        }

        const data = await res.json();
        console.log(data);
        await getCampaignInfo();
    } catch (error) {
        console.error('Error in unassigning ad request.', error);
    }
}

onMounted(async () => {
    await getCampaignInfo();
    if (user.role == 'Influencer') {
        console.log('GET the influencer_id!');
        await fetchInfluencerInfo();
    }
});
</script>

<template>
    <Navbar />
    <section class="my-4">
        <h2 class="mb-3">{{ campaign.name }}</h2>
        <p class="mb-3">{{ campaign.description }}</p>

        <div 
            v-if="user.role == 'Sponsor'" 
            class="mb-4 p-3 border rounded shadow-sm alert alert-light"
        >
            <div class="d-flex align-items-center justify-content-start">
                <p class="mb-0">
                    <strong>Campaign Actions:</strong>
                </p>
                <RouterLink 
                    :to="`/campaign/${campaignId}/edit`" 
                    class="btn btn-warning btn-sm ms-2"
                >
                    Edit
                </RouterLink>
                <button 
                    @click="deleteCampaign" 
                    class="btn btn-danger btn-sm ms-2"
                >
                    Delete
                </button>
            </div>
        </div>

        <h3 class="mt-4">Campaign Info</h3>
        <ul class="mb-4">
            <li>
                <strong>Budget:</strong> Rs. {{ formatNumber(campaign.budget) }}
            </li>
            <li>
                <strong>Duration:</strong> {{ campaign.startDate }} to {{ campaign.endDate }}
            </li>
            <li>
                <strong>Niche:</strong> {{ campaign.niche }}
            </li>
            <li>
                <strong>Visibility:</strong> {{ campaign.visibility }}
            </li>
        </ul>

        <h3 class="mt-4">Ad Requests</h3>
        <p class="text-muted">
            Advertisement requests sent to influencers on the platform. 
        </p>

        <div class="row">
            <div 
                v-for="ad in campaign.adRequests" 
                :key="ad.id" 
                class="col-md-6 mb-3"
            >
                <div class="card shadow-sm h-100">
                    <div class="card-body d-flex flex-column">
                        <h4 class="card-title">{{ ad.requirement }}</h4>
                        <p class="card-text">{{ ad.message }}</p>

                        <ul class="list-unstyled">
                            <li>
                                <strong>Influencer:</strong> {{ ad.influencer.name || '-' }}
                            </li>
                            <li>
                                <strong>Status:</strong> {{ ad.status }}
                            </li>
                            <li>
                                <strong>Payout:</strong> Rs. {{ formatNumber(ad.payment_amount) }}
                            </li>
                        </ul>

                        <div v-if="user.role == 'Sponsor'" class="mt-auto">
                            <div 
                                v-if="ad.status == 'Pending'" 
                            >
                                <div v-if="ad.sender_user_id == userId" class="d-flex gap-2">
                                    <RouterLink 
                                        :to="(ad.influencer.id > 0 && ad.status == 'Pending') ? `/ad-request/${ad.id}/edit?influencer_id=${ad.influencer.id}` : `/ad-request/${ad.id}/edit`" 
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

                                <div v-else class="d-flex gap-2">
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
                            <div v-else-if="ad.status == 'Rejected'" class="d-flex gap-2">
                                <button
                                    @click="unassignAdRequests(ad.id)"
                                    class="btn btn-primary btn-sm"
                                >
                                    Unassign
                                </button>
                                <button 
                                    @click="deleteAdRequest(ad.id)" 
                                    class="btn btn-danger btn-sm"
                                >
                                    Delete
                                </button>
                            </div>
                            <div v-else>
                                <button class="btn btn-light btn-sm" disabled>
                                    Ad request is not available
                                </button>
                            </div>
                        </div>

                        <div v-if="user.role == 'Influencer'" class="mt-auto">
                            <!-- Unassigned Ad Request -->
                            <div
                                v-if="ad.influencer.id == 0" 
                                class="d-flex gap-2"
                            >
                                <button 
                                    @click="acceptAdRequest(ad.id)"
                                    class="btn btn-success btn-sm"
                                >
                                    Accept
                                </button>
                                <RouterLink 
                                    :to="`/ad-request/${ad.id}/negotiate`" 
                                    class="btn btn-warning btn-sm"
                                >
                                    Negotiate
                                </RouterLink>
                            </div>
                            <!-- Assigned To Me (Simple Redirect) -->
                             <div v-else-if="ad.influencer.id == state.influencerId">
                                <RouterLink to="/adverts" class="btn btn-primary btn-sm">
                                    View in Adverts
                                </RouterLink>
                             </div>
                            <div v-else>
                                <button class="btn btn-light btn-sm" disabled>
                                    Ad request is not available
                                </button>
                            </div>
                        </div>

                    </div>
                </div>
            </div>
        </div>

        <div 
            v-if="user.role == 'Sponsor'" 
            class="text-center mt-4"
        >
            <RouterLink 
                :to="`/ad-request/create?campaign_id=${campaignId}`" 
                class="btn btn-outline-primary me-3"
            >
                Create Ad Request
            </RouterLink>
            <RouterLink to="/search" class="btn btn-outline-success">
                Search for Influencers
            </RouterLink>
        </div>

        <!-- <div v-if="campaign.visibility == 'Private'" class="mt-4 text-center">
            <p>*Manual Assignment of Ad Request</p>
        </div> -->

    </section>
</template>
