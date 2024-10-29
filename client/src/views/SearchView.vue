<script setup>
import Navbar from '@/components/Navbar.vue';
import SearchInfluencers from '@/components/search/SearchInfluencers.vue';
import SearchCampaigns from '@/components/search/SearchCampaigns.vue';
import SearchUsers from '@/components/search/SearchUsers.vue';

const userRole = JSON.parse(localStorage.getItem('user')).role;
</script>

<template>
    <Navbar />
    <div v-if="userRole == 'Sponsor'">
        <SearchInfluencers />
    </div>
    <div v-else-if="userRole == 'Influencer'">
        <SearchCampaigns />
    </div>
    <div v-else>
        <SearchUsers />
    </div>
</template>
