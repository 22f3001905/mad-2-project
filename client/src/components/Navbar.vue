<script setup>
import { RouterLink, useRouter } from 'vue-router';
import { reactive, computed } from 'vue';
import { useUserStore } from '@/stores/user';

const router = useRouter();
const store = useUserStore();
const isLoggedIn = computed(() => store.isLoggedIn);

const logoutUser = async () => {
    try {
        await fetch('/api/logout');
        sessionStorage.removeItem('authToken');
        store.logout();
        sessionStorage.removeItem('userEmail');
        router.push('/');
    } catch (error) {
        console.error('Error logging out.', error);
    }
}
</script>

<template>
    <nav>
        <div>SponsorConnect</div>
        <ul>
            <li v-if="isLoggedIn">
                <RouterLink to="/dashboard">Dashboard</RouterLink>
            </li>
            <li>
                <button v-if="isLoggedIn" @click="logoutUser">Logout</button>
                <RouterLink v-else to="/login">Login</RouterLink>
            </li>
        </ul>
    </nav>
</template>
