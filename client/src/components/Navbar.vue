<script setup>
import { RouterLink, useRouter } from 'vue-router';
import { reactive, computed, defineProps, ref } from 'vue';
import { useUserStore } from '@/stores/user';
import { clearCookie } from '@/utils';

const router = useRouter();

const store = useUserStore();
const userRole = computed(() => store.getUserRole);
const isLoggedIn = computed(() => store.getAuthToken != null);

const logoutUser = async () => {
    try {
        await fetch('/api/logout');
        localStorage.removeItem('authToken');
        localStorage.removeItem('user');
        store.logout();
        clearCookie('session');
        router.push('/');
    } catch (error) {
        console.error('Error logging out.', error);
    }
}
</script>

<template>
    <nav class="navbar justify-content-end">
        <div class="container-fluid">
            <RouterLink class="navbar-brand" to="/">💻 SponsorConnect</RouterLink>
            <ul class="nav" v-if="isLoggedIn">
                <li class="nav-item">
                    <RouterLink class="nav-link" to="/dashboard">Dashboard</RouterLink>
                </li>
                <li class="nav-item">
                    <RouterLink class="nav-link" to="/stats">Stats</RouterLink>
                </li>
                <li class="nav-item">
                    <RouterLink v-if="userRole == 'Sponsor'" class="nav-link" to="/campaigns">Campaigns</RouterLink>
                    <RouterLink v-else-if="userRole == 'Influencer'" class="nav-link" to="/adverts">Adverts</RouterLink>
                </li>
                <li class="nav-item">
                    <RouterLink class="nav-link" to="/search">Search</RouterLink>
                </li>
                <li class="nav-item">
                    <button class="nav-link" @click="logoutUser">Logout</button>
                </li>
            </ul>
            <ul class="nav" v-else>
                <li class="nav-item">
                    <RouterLink class="nav-link" to="/about">About</RouterLink>
                </li>
                <li class="nav-item">
                    <RouterLink class="nav-link" to="/register">Register</RouterLink>
                </li>
                <li class="nav-item">
                    <RouterLink class="nav-link" to="/login">Login</RouterLink>
                </li>
            </ul>
        </div>
    </nav>
</template>
