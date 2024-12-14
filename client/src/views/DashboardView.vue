<script setup>
import { onMounted, reactive } from 'vue';

import Navbar from '@/components/Navbar.vue';
import UserInfo from '@/components/UserInfo.vue';
import ApproveSponsor from '@/components/ApproveSponsor.vue';
import ActiveCampaignList from '@/components/campaign/ActiveCampaignList.vue';
import PendingAdRequestList from '@/components/ad-request/PendingAdRequestList.vue';

import { formatNumber, redirectToErrorPage } from '@/utils';
import { useRouter } from 'vue-router';

const router = useRouter();

const user = reactive({
    id: null,
    name: '',
    email: '',
    role: ''
});

const sponsor = reactive({
    budget: 0,
    industry: '',
    campaigns: []
});
const influencer = reactive({
    niche: '',
    reach: 0,
    wallet_balance: 0,
    category: '',
    assigned_ads: []
});

onMounted(async () => {
    // fetch sponsor/influencer data
    try {
        const res = await fetch('/api/info/user', {
            headers: { 'Authentication-Token': localStorage.getItem('authToken') }
        });

        if (!res.ok) {
            return redirectToErrorPage(res.status, router);
        }

        const data = await res.json();
        // console.log(data);
        user.id = data.id;
        user.email = data.email;
        user.role = data.role;
    } catch (error) {
        console.error('Error in fetching user info.', error);
    }
    if (user.role == 'Sponsor') {
        try {
            const res = await fetch('/api/info/sponsor', {
                headers: { 'Authentication-Token': localStorage.getItem('authToken') }
            });

            if (!res.ok) {
                return redirectToErrorPage(res.status, router);
            }

            const data = await res.json();

            console.log(data);
            user.name = data.name;
            sponsor.budget = data.budget;
            sponsor.industry = data.industry;
            sponsor.campaigns = data.campaigns;
        } catch (error) {
            console.error('Error in fetching sponsor info.', error);
        }
    } else if (user.role == 'Influencer') {
        try {
            const res = await fetch('/api/info/influencer', {
                headers: { 'Authentication-Token': localStorage.getItem('authToken') }
            });

            if (!res.ok) {
                return redirectToErrorPage(res.status, router);
            }

            const data = await res.json();
            console.log(data);
            user.name = data.name;
            influencer.niche = data.niche;
            influencer.reach = data.reach;
            influencer.wallet_balance = data.wallet_balance;
            influencer.category = data.category;
            influencer.assigned_ads = data.assigned_ads;
        } catch (error) {
            console.error('Error in fetching influencer info.', error);
        }
    } else {
        user.name = 'Admin';
        user.role = 'Admin';
    }
});
</script>

<template>
    <Navbar />
    <UserInfo 
        :user="user" 
        :sponsor="{ budget: sponsor.budget, industry: sponsor.industry }" 
        :influencer="{ niche: influencer.niche, reach: influencer.reach, wallet_balance: influencer.wallet_balance, category: influencer.category }" 
    />
    <ApproveSponsor v-if="user.role == 'Admin'" />
    <ActiveCampaignList :role="user.role" />
    <PendingAdRequestList v-if="user.name && user.role != 'Admin'" />
</template>
