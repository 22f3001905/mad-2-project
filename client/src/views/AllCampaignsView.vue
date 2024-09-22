<script setup>
import Navbar from '@/components/Navbar.vue';
import CampaignList from '@/components/CampaignList.vue';
import { RouterLink } from 'vue-router';

</script>

<template>
    <Navbar />
    <CampaignList />
    <RouterLink to="/campaign/create">Create Campaign</RouterLink>
</template>
