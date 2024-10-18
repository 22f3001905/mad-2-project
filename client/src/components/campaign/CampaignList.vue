<script setup>
import { ref, defineProps, reactive, onMounted } from 'vue';
import { RouterLink } from 'vue-router';

const state = reactive({
    campaigns: []
});
const user = JSON.parse(localStorage.getItem('user'));

onMounted(async () => {
    try {
        const res = await fetch(`/api/${user.role == 'Sponsor' ? 'sponsor' : 'influencer'}/campaigns`, {
            method: 'GET',
            headers: { 'Authentication-Token': localStorage.getItem('authToken') }
        });
        const data = await res.json();
        console.log(data.campaigns);
        state.campaigns = [...data.campaigns];  // creates a copy
    } catch (error) {
        console.error('Error fetching all the campaigns for this user.', error);
    }
});
</script>

<template>
    <section>
        <h2>{{ user.role == 'Influencer' ? 'Public' : '' }} Campaign List</h2>
        <div>
            <div v-for="campaign in state.campaigns" style="border: 1px solid black;">
                <h3>{{ campaign.name }}</h3>
                <p>{{ campaign.description }}</p>
                <p>Starts: {{ new Date(campaign.start_date).toDateString() }} | Ends: {{ new Date(campaign.end_date).toDateString() }}</p>
                <p>{{ campaign.visibility }}</p>
                <p>Budget: Rs. {{ campaign.budget }}</p>
                <p>Niche: {{ campaign.niche }}</p>
                <div>
                    <RouterLink :to="`/campaign/${campaign.id}`">View</RouterLink>
                </div>
            </div>
        </div>
    </section>
</template>
