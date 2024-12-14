<script setup>
import { reactive, onMounted, ref } from 'vue';
import Navbar from '@/components/Navbar.vue';

import { formatNumber, redirectToErrorPage } from '@/utils';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();
const influencerId = ref(route.params.id);

const influencer = reactive({
    name: '',
    email: '',
    niche: '',
    reach: 0,
    wallet_balance: 0,
    category: '',
    assigned_ads: []
});

onMounted(async () => {
    try {
        const res = await fetch(`/api/info/influencer?influencerId=${influencerId.value}`, {
            headers: { 'Authentication-Token': localStorage.getItem('authToken') }
        });

        if (!res.ok) {
            return redirectToErrorPage(res.status, router);
        }

        const data = await res.json();
        console.log(data);

        influencer.name = data.name;
        influencer.email = data.email,
        influencer.niche = data.niche;
        influencer.reach = data.reach;

        influencer.wallet_balance = data.wallet_balance;
        influencer.category = data.category;
        influencer.assigned_ads = data.assigned_ads;

    } catch (error) {
        console.error('Error in fetching influencer info.', error);
    }
});
</script>

<template>
    <Navbar />
    <section class="pt-4">
        <h2 class="mb-3">Influencer Profile</h2>
        <ul>
            <li>
                <strong>Name:</strong> {{ influencer.name }}
            </li>
            <li>
                <strong>Email:</strong> {{ influencer.email }}
            </li>
            <div>
                <li style="max-width: 400px;">
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
    <section>
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
