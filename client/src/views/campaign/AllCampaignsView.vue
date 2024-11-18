<script setup>
import Navbar from '@/components/Navbar.vue';
import CampaignList from '@/components/campaign/CampaignList.vue';
import { RouterLink } from 'vue-router';

const user = JSON.parse(localStorage.getItem('user'));
</script>

<template>
    <Navbar />
    <CampaignList />
    <div class="d-flex justify-content-center my-4">
        <RouterLink 
            v-if="user.role == 'Sponsor'" 
            to="/campaign/create" 
            class="btn btn-outline-success"
        >
            Create Campaign
        </RouterLink>
    </div>
</template>
