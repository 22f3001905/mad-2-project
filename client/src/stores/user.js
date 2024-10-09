import { ref, computed, reactive } from 'vue';
import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', () => {
    const loggingStatus = ref(localStorage.getItem('authToken') != null);
    const isLoggedIn = computed(() => loggingStatus.value);
    
    function login() {
        loggingStatus.value = true;
    }
    function logout() {
        loggingStatus.value = false;
    }
    
    return { loggingStatus, isLoggedIn, login, logout };
});
