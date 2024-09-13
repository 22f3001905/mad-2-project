<script setup>
import Login from '@/components/Login.vue';
import Navbar from '@/components/Navbar.vue';

import { userLoggedInRedirect } from '@/utils';
userLoggedInRedirect();
</script>

<template>
    <section>
        <Navbar />
        <h1>Login</h1>
        <Login />
    </section>
</template>
