<script setup>
import Login from '@/components/Login.vue';
import Navbar from '@/components/Navbar.vue';

import { useUserStore } from '@/stores/user';
import { useRouter } from 'vue-router';

const store = useUserStore();
const router = useRouter();
if (store.isLoggedIn) {
    router.push('/');
}
</script>

<template>
    <section>
        <Navbar />
        <h1>Login</h1>
        <Login />
    </section>
</template>
