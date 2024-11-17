<script setup>
import Navbar from '@/components/Navbar.vue';
import Register from '@/components/auth/Register.vue';

import { userLoggedInRedirect } from '@/utils';
userLoggedInRedirect();
</script>

<template>
    <Navbar />
    <Register />
</template>
