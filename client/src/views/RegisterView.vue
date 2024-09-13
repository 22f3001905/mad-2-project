<script setup>
import Navbar from '@/components/Navbar.vue';
import Register from '@/components/Register.vue';

import { userLoggedInRedirect } from '@/utils';
userLoggedInRedirect();
</script>

<template>
    <Navbar />
    <h1>Account Registration</h1>
    <Register />
</template>
