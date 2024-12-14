<script setup>
import  { defineProps } from 'vue';
import { RouterLink } from 'vue-router';

defineProps({
    statusCode: {
        type: Number,
        default: 500
    },
    description: {
        type: String,
        default: 'Something went wrong. Please try again later.'
    }
});
</script>

<template>
    <div class="text-center mt-5 p-5 border rounded shadow-sm bg-light">
        <h2 class="display-1 text-danger">{{ statusCode }}</h2>
        <p class="lead text-muted">{{ description }}</p>
        <RouterLink to="/" class="btn btn-primary mt-3">Home</RouterLink>
    </div>
</template>
