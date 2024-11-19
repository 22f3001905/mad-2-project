<script setup>
import  { defineProps } from 'vue';
import { formatNumber } from '@/utils';
import { RouterLink } from 'vue-router';

defineProps({
    user: Object,
    sponsor: Object,
    influencer: Object,
});
</script>

<template>
    <section class="pt-4">
        <h2 class="mb-3">Account Details</h2>
        <ul>
            <li>
                <strong>Name:</strong> {{ user.name }}
            </li>
            <li>
                <strong>Email:</strong> {{ user.email }}
            </li>
            <div v-if="user.role == 'Sponsor'">
                <li>
                    <strong>Budget:</strong> Rs. {{ formatNumber(sponsor.budget) }}
                    <ul>
                        <li>
                            <RouterLink to="/add-money">Add Money</RouterLink>
                        </li>
                    </ul>
                </li>
                <li>
                    <strong>Industry:</strong> {{ sponsor.industry }}
                </li>
            </div>
            <div v-else-if="user.role == 'Influencer'">
                <li style="max-width: 400px;">
                    <strong>Niche: </strong>
                    <span 
                        class="badge bg-dark me-1" 
                        v-for="tag in influencer.niche.split(', ')"
                    >
                    {{ tag }}
                    </span>
                </li>
                <li>
                    <strong>Reach:</strong> {{ formatNumber(influencer.reach) }} people
                </li>
                <li>
                    <strong>Wallet:</strong> Rs. {{ formatNumber(influencer.wallet_balance) }}
                </li>
                <li>
                    <strong>Category:</strong> {{ influencer.category }}
                </li>
            </div>
        </ul>
    </section>
</template>
