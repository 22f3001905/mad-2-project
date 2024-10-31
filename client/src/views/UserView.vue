<script setup>
import { ref, reactive, onMounted } from 'vue';
import Navbar from '@/components/Navbar.vue';
import { useRoute } from 'vue-router';

const route = useRoute();
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
    <h2>Account Details</h2>
    <ul>
        <li>Email: {{ user.email }}</li>
        <div v-if="user.role == 'Sponsor' || user.role == 'Influencer'">
            <li>Name: {{ user.name }}</li>
            <li>Flagged: {{ user.flagged }}</li>
        </div>
        <div v-else>
            <li>User: ADMIN</li>
        </div>
        <div v-if="user.role == 'Sponsor'">
            <li>Budget: Rs. {{ sponsor.budget }}</li>
            <li>Industry: {{ sponsor.industry }}</li>
        </div>
        <div v-else-if="user.role == 'Influencer'">
            <li>Niche: {{ influencer.niche }}</li>
            <li>Reach: {{ influencer.reach }} people</li>
            <li>Wallet: Rs. {{ influencer.wallet_balance }}</li>
            <li>Category: {{ influencer.category }}</li>
        </div>
    </ul>
    <section v-if="user.role == 'Sponsor'">
        <h3>Campaigns</h3>
        <div v-for="campaign in sponsor.campaigns">
            <p>{{ campaign.name }}</p>
            <ul>
                <li>Ends: {{ new Date(campaign.end_date).toDateString() }}</li>
                <li>Visibility: {{ campaign.visibility }}</li>
                <li>Flagged: {{ campaign.flagged }}</li>
            </ul>
        </div>
        <div v-if="sponsor.campaigns.length == 0">
            <p>None</p>
        </div>
    </section>
    <section v-else>
        <h3>Assigned Ads</h3>
        <div v-for="ad in influencer.assigned_ads">
            <p>{{ ad.requirement }}</p>
            <ul>
                <li>Status: {{ ad.status }}</li>
                <li>Payout: Rs. {{ ad.payment_amount }}</li>
            </ul>
        </div>
        <div v-if="influencer.assigned_ads.length == 0">
            <p>None</p>
        </div>
    </section>
</template>
