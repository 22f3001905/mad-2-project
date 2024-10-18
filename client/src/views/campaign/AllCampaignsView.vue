<script setup>
import Navbar from '@/components/Navbar.vue';
import CampaignList from '@/components/campaign/CampaignList.vue';
import { RouterLink } from 'vue-router';

const user = JSON.parse(localStorage.getItem('user'));
</script>

<template>
    <Navbar />
    <CampaignList />
    <RouterLink v-if="user.role == 'Sponsor'" to="/campaign/create">Create Campaign</RouterLink>
</template>
