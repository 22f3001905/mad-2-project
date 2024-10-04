<script setup>
import Navbar from '@/components/Navbar.vue';
import SearchInfluencers from '@/components/SearchInfluencers.vue';
import SearchCampaigns from '@/components/SearchCampaigns.vue';

const userRole = JSON.parse(sessionStorage.getItem('user')).role;
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
