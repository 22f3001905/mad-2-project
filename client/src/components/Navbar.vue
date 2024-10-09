<script setup>
import { RouterLink, useRouter } from 'vue-router';
import { reactive, computed, defineProps } from 'vue';
import { useUserStore } from '@/stores/user';
import { clearCookie } from '@/utils';

// const props = defineProps({
//     role: String  // ['Admin', 'Sponsor', 'Influencer']
// });

const user = JSON.parse(localStorage.getItem('user'));

const router = useRouter();
const store = useUserStore();
const isLoggedIn = computed(() => store.isLoggedIn);

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
            <ul class="nav">
                <li v-if="isLoggedIn" class="nav-item"><RouterLink class="nav-link" to="/dashboard">Dashboard</RouterLink></li>
                <li v-if="isLoggedIn && user.role == 'Sponsor'" class="nav-item"><RouterLink class="nav-link" to="/campaigns">Campaigns</RouterLink></li>
                <li v-if="isLoggedIn && user.role == 'Influencer'" class="nav-item"><RouterLink class="nav-link" to="/profile">Profile</RouterLink></li>
                <li v-if="isLoggedIn" class="nav-item"><RouterLink class="nav-link" to="/search">Search</RouterLink></li>
                <li class="nav-item">
                    <button class="nav-link" v-if="isLoggedIn" @click="logoutUser">Logout</button>
                    <RouterLink class="nav-link" v-else to="/login">Login</RouterLink>
                </li>
            </ul>
        </div>
    </nav>
</template>
