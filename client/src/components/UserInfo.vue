<script setup>
import  { defineProps } from 'vue';

defineProps({
    user: Object,
    sponsor: Object,
    influencer: Object,
});
</script>

<template>
    <section>
        <h2>Account Details</h2>
        <ul>
            <li>Email: {{ user.email }}</li>
            <div v-if="user.role == 'Sponsor'">
                <li>Budget: Rs. {{ sponsor.budget }} <button>Add Money</button></li>
                <li>Industry: {{ sponsor.industry }}</li>
            </div>
            <div v-else-if="user.role == 'Influencer'">
                <li>Niche: {{ influencer.niche }}</li>
                <li>Reach: {{ influencer.reach }} people</li>
                <li>Wallet: Rs. {{ influencer.wallet_balance }}</li>
                <li>Category: {{ influencer.category }}</li>
            </div>
            <div v-else>
                <li>User: ADMIN</li>
            </div>
        </ul>
    </section>
</template>
