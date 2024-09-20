<script setup>
import { defineProps } from 'vue';

defineProps({
    title: String  // 'Create' or 'Edit'
});
</script>

<template>
    <h1>{{ title }} Campaign</h1>
    <form></form>
</template>
