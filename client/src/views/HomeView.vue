<script setup>
import Navbar from '@/components/Navbar.vue';
import { computed } from 'vue';
import { RouterLink } from 'vue-router';
import { useUserStore } from '@/stores/user';

const store = useUserStore();
const userName = computed(() => store.getUserName);
const isLoggedIn = computed(() => store.getAuthToken != null);
</script>

<template>
    <main>
        <Navbar />
        <h1 class="pt-2 mb-4">SponsorConnect</h1>
        <p class="lead mb-5">
            An Influencer Engagement & Sponsorship Co-ordination Platform.
        </p>
        <div class="row align-items-center">
            <figure class="text-center col-8">
                <img 
                    class="img-fluid rounded shadow" 
                    src="/img/work.jpg" 
                    alt="A picture of a modern workplace." 
                    style="max-height: 500px;" 
                />
                <figcaption 
                    class="text-muted fs-6 mt-2 fst-italic" 
                    style="font-size: 0.75rem !important;"
                >
                    Photo by Glenn Carstens-Peters on 
                    <a 
                        href="https://unsplash.com/photos/person-using-macbook-pro-npxXWgQ33ZQ?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash" 
                        target="_blank"
                    >
                        Unsplash
                    </a>
                </figcaption>
            </figure>
            <div v-if="isLoggedIn" class="col-4 text-center">
                <h3>Welcome, {{ userName }}</h3>
                <div>
                    Go to <RouterLink to="/dashboard">Dashboard</RouterLink>
                </div>
            </div>
            <div v-else class="col-4 text-center">
                <h3>Actions</h3>
                <div>
                    <RouterLink to="/login">Login</RouterLink>
                    <span> or </span>
                    <RouterLink to="/register">Register</RouterLink>
                </div>
            </div>
        </div>
    </main>
</template>

<style scoped></style>
