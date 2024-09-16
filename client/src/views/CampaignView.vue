<script setup>
import { ref } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const campaignId = ref(route.params.id);
</script>

<template>
    <h1>Campaign with ID: {{ campaignId }}</h1>
</template>
