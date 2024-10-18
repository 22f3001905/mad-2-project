<script setup>
import Navbar from '@/components/Navbar.vue';
import SponsorStats from '@/components/stats/SponsorStats.vue';
import InfluencerStats from '@/components/stats/InfluencerStats.vue';

const userRole = JSON.parse(localStorage.getItem('user')).role;
</script>

<template>
    <Navbar />
    <div v-if="userRole == 'Sponsor'">
        <SponsorStats />
    </div>
    <div v-else>
        <InfluencerStats />
    </div>
</template>
