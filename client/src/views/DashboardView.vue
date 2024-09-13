<script setup>
import { onMounted } from 'vue';

import Navbar from '@/components/Navbar.vue';
import { userLoggedInRedirect } from '@/utils';
import { useUserStore } from '@/stores/user';
import router from '@/router';

const store = useUserStore();
if (!store.isLoggedIn) {
    router.push('/login');
}
const userEmail = sessionStorage.getItem('userEmail');

onMounted(() => {
    // fetch sponsor/influencer data
});
</script>

<template>
    <Navbar />
    <h1>Welcome, {{ userEmail }}</h1>
</template>
