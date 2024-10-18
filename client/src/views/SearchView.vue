<script setup>
import Navbar from '@/components/Navbar.vue';
import SearchInfluencers from '@/components/search/SearchInfluencers.vue';
import SearchCampaigns from '@/components/search/SearchCampaigns.vue';

const userRole = JSON.parse(localStorage.getItem('user')).role;
</script>

<template>
    <Navbar :role="userRole" />
    <div v-if="userRole == 'Sponsor'">
        <SearchInfluencers />
    </div>
    <div v-else>
        <SearchCampaigns />
    </div>
</template>
