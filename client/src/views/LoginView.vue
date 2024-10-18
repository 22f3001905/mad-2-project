<script setup>
import Login from '@/components/auth/Login.vue';
import Navbar from '@/components/Navbar.vue';

import { userLoggedInRedirect, clearCookie } from '@/utils';
const redirect = userLoggedInRedirect();
// Clear session cookie if user not logged in!
if (!redirect) {
    clearCookie('session');
}
</script>

<template>
    <section>
        <Navbar />
        <h1>Login</h1>
        <Login />
    </section>
</template>
