import { ref, computed, reactive } from 'vue';
import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', () => {
    const user = reactive(JSON.parse(localStorage.getItem('user')) || { id: '', email: '', role: '' });
    const authToken = ref(localStorage.getItem('authToken') || null);

    const getUserId = computed(() => user.id);
    const getUserRole = computed(() => user.role);
    const getUserName = computed(() => user.name);
    const getAuthToken = computed(() => authToken.value);

    function logout() {
        authToken.value = null;
        user.id = '';
        user.email = '';
        user.role = '';
        user.name = '';
    }
    function login() {
        authToken.value = localStorage.getItem('authToken');

        const loggedInUser = JSON.parse(localStorage.getItem('user'));
        user.id = loggedInUser.id;
        user.email = loggedInUser.email;
        user.role = loggedInUser.role;
        user.name = loggedInUser.name;
    }

    return { getUserId, getUserRole, getAuthToken, getUserName, logout, login };
});
