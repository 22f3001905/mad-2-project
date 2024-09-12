<script setup>
import { RouterLink } from 'vue-router';
import { reactive, computed } from 'vue';
import { useUserStore } from '@/stores/user';

const store = useUserStore();
const isLoggedIn = computed(() => store.isLoggedIn);

const logoutUser = async () => {
    try {
        await fetch('/api/logout');
        sessionStorage.removeItem('authToken');
        store.logout();
    } catch (error) {
        console.error('Error logging out.', error);
    }
}
</script>

<template>
    <nav>
        <div>SponsorConnect</div>
        <ul>
            <li>
                <RouterLink to="/dashboard">Dashboard</RouterLink>
            </li>
            <li>
                <button v-if="isLoggedIn" @click="logoutUser">Logout</button>
                <RouterLink v-else to="/login">Login</RouterLink>
            </li>
        </ul>
    </nav>
</template>
