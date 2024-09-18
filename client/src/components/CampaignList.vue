<script setup>
import { defineProps } from 'vue';
import { RouterLink } from 'vue-router';

defineProps({
    campaigns: Array
});
</script>

<template>
    <section>
        <h2>Active Campaigns</h2>
        <div>
            <div v-for="campaign in campaigns" style="border: 1px solid black;">
                <h3>{{ campaign.name }}</h3>
                <p>{{ campaign.description }}</p>
                <p>Ends: {{ new Date(campaign.end_date).toDateString() }}</p>
                <p>{{ campaign.visibility }}</p>
                <p>Niche: {{ campaign.niche }}</p>
                <!-- <p>Flagged: {{ campaign.flagged }}</p> -->
                <div>
                    <RouterLink :to="`/campaign/${campaign.id}`">View</RouterLink>
                </div>
            </div>
        </div>
    </section>
</template>
