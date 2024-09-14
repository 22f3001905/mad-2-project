<script setup>
import { onMounted, reactive } from 'vue';

import Navbar from '@/components/Navbar.vue';
import { userLoggedInRedirect } from '@/utils';

const user = reactive({
    name: '',
    email: '',
    role: ''
});

const sponsor = reactive({
    // name: '',
    budget: 0,
    industry: '',
    campaigns: []
});
const influencer = reactive({
    // name: '',
    niche: '',
    reach: 0,
    wallet_balance: 0,
    category: '',
    assigned_ads: []
});

onMounted(async () => {
    // fetch sponsor/influencer data
    try {
        const res = await fetch('/api/user/info', {
            headers: { 'Authentication-Token': sessionStorage.getItem('authToken') }
        });
        const data = await res.json();
        user.email = data.email;
        user.role = data.role;
    } catch (error) {
        console.error('Error in fetching user info.', error);
    }
    if (user.role == 'Sponsor') {
        try {
            const res = await fetch('/api/sponsor/info', {
                headers: { 'Authentication-Token': sessionStorage.getItem('authToken') }
            });
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
            const res = await fetch('/api/influencer/info', {
                headers: { 'Authentication-Token': sessionStorage.getItem('authToken') }
            });
            const data = await res.json();
            console.log(data);
            user.name = data.name;
        } catch (error) {
            console.error('Error in fetching influencer info.', error);
        }
    }
});
</script>

<template>
    <Navbar />
    <h1>Welcome, {{ user.name }}</h1>
</template>
