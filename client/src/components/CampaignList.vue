<script setup>
import { ref, defineProps, reactive, onMounted } from 'vue';
import { RouterLink } from 'vue-router';

const showAllCampaigns = ref(false);
const props = defineProps({
    campaigns: Array
});
const state = reactive({
    campaigns: []
});

if (props.campaigns) {
    console.log('Campaigns included in props.');
    showAllCampaigns.value = true;
} else {
    console.log('No campaigns included.');
    showAllCampaigns.value = false;
}

onMounted(async () => {
    try {
        const res = await fetch('/api/all-campaigns', {
            method: 'GET',
            headers: { 'Authentication-Token': sessionStorage.getItem('authToken') }
        });
        const data = await res.json();
        console.log(data);
    } catch (error) {
        console.error('Error fetching all the campaigns for this user.', error);
    }
});
</script>

<template>
    <section>
        <h2>{{ showAllCampaigns ? 'Active' : 'All' }} Campaigns</h2>
        <div v-if="showAllCampaigns">
            <div v-for="campaign in campaigns" style="border: 1px solid black;">
                <h3>{{ campaign.name }}</h3>
                <p>Ends: {{ new Date(campaign.end_date).toDateString() }}</p>
                <p>{{ campaign.visibility }}</p>
                <!-- <p>Flagged: {{ campaign.flagged }}</p> -->
                <div>
                    <RouterLink :to="`/campaign/${campaign.id}`">View</RouterLink>
                </div>
            </div>
        </div>
        <div v-else>
            <div v-for="campaign in state.campaigns" style="border: 1px solid black;">
            </div>
        </div>
    </section>
</template>
