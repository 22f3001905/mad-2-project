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
    <h2 class="text-center mb-3 pt-2">Login Form</h2>
    <div v-if="state.incorrectCreds">
        <p>Incorrect email/password, please try again.</p>
    </div>
    <div class="row justify-content-center">
        <div class="col-md-6">
            <form @submit.prevent="loginUser" class="p-4 border rounded shadow-sm">
                <div class="mb-3">
                    <label for="email" class="form-label">Email</label>
                    <input class="form-control" v-model="form.email" type="email" name="email" id="email" required autocomplete="email" />
                </div>
                <div class="mb-3">
                    <label for="password" class="form-label">Password</label>
                    <input class="form-control" v-model="form.password" type="password" name="password" id="password" required autocomplete="current-password" />
                </div>
                <div class="mb-3">
                    <button class="btn btn-primary" type="submit">Login</button>
                </div>
            </form>
            <div class="mt-4">
                <p>Don't have an account? <RouterLink to="/register">Register</RouterLink></p>
            </div>
        </div>
    </div>
</template>
