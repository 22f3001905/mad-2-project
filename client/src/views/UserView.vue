<script setup>
import { ref, reactive, onMounted } from 'vue';
import Navbar from '@/components/Navbar.vue';
import { useRoute, useRouter } from 'vue-router';
import { formatNumber, redirectToErrorPage } from '@/utils';

const route = useRoute();
const router = useRouter();
const userId = ref(route.params.id);

const user = reactive({
    email: null,
    role: null,
    flagged: null,
    name: null,
    wallet: null,
});

const sponsor = reactive({
    budget: null,
    industry: null,
    campaigns: []
});

const influencer = reactive({
    niche: null,
    reach: null,
    wallet_balance: null,
    category: null,
    assigned_ads: []
});

onMounted(async () => {
    try {
        const res = await fetch(`/api/user/${userId.value}`, {
            headers: { 'Authentication-Token': localStorage.getItem('authToken') }
        });

        if (!res.ok) {
            return redirectToErrorPage(res.status, router);
        }

        const data = await res.json();
        console.log(data.data);

        user.email = data.data.email;
        user.role = data.data.role;
        user.flagged = data.data.flagged;
        user.name = data.data.name;
        user.wallet = data.data.wallet;
    } catch (error) {
        console.error('Error in fetching info.', error);
    }

    if (user.role == 'Sponsor') {
        try {
            const res = await fetch(`/api/info/sponsor?userId=${userId.value}`, {
                headers: { 'Authentication-Token': localStorage.getItem('authToken') }
            });

            if (!res.ok) {
                return redirectToErrorPage(res.status, router);
            }

            const data = await res.json();
            console.log(data);

            sponsor.budget = data.budget;
            sponsor.industry = data.industry;
            sponsor.campaigns = data.campaigns;
        } catch (error) {
            console.error('Error in fetching sponsor info.', error);
        }
    } else if (user.role == 'Influencer') {
        try {
            const res = await fetch(`/api/info/influencer?userId=${userId.value}`, {
                headers: { 'Authentication-Token': localStorage.getItem('authToken') }
            });

            if (!res.ok) {
                return redirectToErrorPage(res.status, router);
            }
            
            const data = await res.json();
            console.log(data);

            influencer.niche = data.niche;
            influencer.reach = data.reach;
            influencer.wallet_balance = data.wallet_balance;
            influencer.category = data.category;
            influencer.assigned_ads = data.assigned_ads;
        } catch (error) {
            console.error('Error in fetching influencer info.', error);
        }
    }
});
</script>

<template>
    <Navbar />
    <section class="pt-4">
        <h2 class="mb-3">Account Details</h2>
        <ul>
            <li>
                <strong>Name:</strong> {{ user.name }}
            </li>
            <li>
                <strong>Email:</strong> {{ user.email }}
            </li>
            <div v-if="user.role == 'Sponsor'">
                <li>
                    <strong>Budget:</strong> Rs. {{ formatNumber(sponsor.budget) }}
                </li>
                <li>
                    <strong>Industry:</strong> {{ sponsor.industry }}
                </li>
            </div>
            <div v-else-if="user.role == 'Influencer'">
                <li style="max-width: 400px;" v-if="influencer.niche">
                    <strong>Niche: </strong>
                    <span 
                        class="badge bg-dark me-1" 
                        v-for="tag in influencer.niche.split(', ')"
                    >
                    {{ tag }}
                    </span>
                </li>
                <li>
                    <strong>Reach:</strong> {{ formatNumber(influencer.reach) }} people
                </li>
                <li>
                    <strong>Wallet:</strong> Rs. {{ formatNumber(influencer.wallet_balance) }}
                </li>
                <li>
                    <strong>Category:</strong> {{ influencer.category }}
                </li>
            </div>
        </ul>
    </section>

    <section v-if="user.role == 'Sponsor'">
        <div class="row">
            <div 
                v-for="campaign in sponsor.campaigns" 
                :key="campaign.id" 
                class="col-md-4 mb-4"
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
        <div class="row" v-if="sponsor.campaigns.length == 0">
            <p class="text-muted">
                No campaigns created yet.
            </p>
        </div>
    </section>
    <section v-else>
        <div class="row">
            <div 
                v-for="ad in influencer.assigned_ads" 
                :key="ad.id" 
                class="col-md-6 mb-4" 
            >
                <div class="card shadow-sm h-100">
                    <div class="card-body d-flex flex-column">
                        <h3 class="card-title">{{ ad.requirement }}</h3>
                        <p class="card-text">{{ ad.message }}</p>

                        <ul class="list-unstyled">
                            <li>
                                <strong>Campaign:</strong> {{ ad.campaign.name }}
                            </li>
                            <li>
                                <strong>Status:</strong> {{ ad.status }}
                            </li>
                            <li>
                                <strong>Payout:</strong> Rs. {{ formatNumber(ad.payment_amount) }}
                            </li>
                        </ul>

                        <div class="mt-auto">
                            <RouterLink :to="`/campaign/${ad.campaign.id}`" class="btn btn-primary btn-sm">
                                View Campaign
                            </RouterLink>
                        </div>

                    </div>
                </div>
            </div>
            <div class="row" v-if="influencer.assigned_ads.length == 0">
                <p class="text-muted">
                    No ad requests assigned yet.
                </p>
            </div>
        </div>
    </section>

</template>
