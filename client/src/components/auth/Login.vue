<script setup>
import { reactive } from 'vue';
import { useUserStore } from '@/stores/user';
import { useRouter, RouterLink } from 'vue-router';

const form = reactive({
    email: '',
    password: ''
});

const state = reactive({
    incorrectCreds: false
});

const store = useUserStore();
const router = useRouter();

async function fetchUserInfo(authenticationToken) {
    try {
        const res = await fetch('/api/info/user', {
            headers: { 'Authentication-Token': authenticationToken }
        });
        const data = await res.json();
        console.log(data);
        localStorage.setItem('user', JSON.stringify(data));
    } catch (error) {
        console.error('Error in fetching user info.', error);
    }
}

const loginUser = async () => {
    try {
        const response = await fetch('/api/login?include_auth_token', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(form)
        });
        const data = await response.json();
        console.log(data);

        if (data.response.errors) {
            state.incorrectCreds = true;
            form.password = '';
        } else {
            state.incorrectCreds = false;
            const authenticationToken = data.response.user.authentication_token;
            localStorage.setItem('authToken', authenticationToken);
            const res = await fetchUserInfo(authenticationToken);
            store.login();
            router.push('/dashboard');
        }
    } catch (error) {
        console.error('Error logging in.', error);
    }
}
</script>

<template>
    <section>
        <div v-if="state.incorrectCreds">
            <p>Incorrect email/password, please try again.</p>
        </div>
        <form @submit.prevent="loginUser">
            <div>
                <label for="email">Email</label>
                <input v-model="form.email" type="email" name="email" id="email" required autocomplete="email" />
            </div>
            <div>
                <label for="password">Password</label>
                <input v-model="form.password" type="password" name="password" id="password" required autocomplete="current-password" />
            </div>
            <div>
                <button type="submit">Login</button>
            </div>
        </form>
        <div>
            <p>Don't have an account? <RouterLink to="/register">Register</RouterLink></p>
        </div>
    </section>
</template>
