import { createRouter, createWebHistory } from 'vue-router';

// {
//   path: '/about',
//   name: 'about',
//   // route level code-splitting
//   // this generates a separate chunk (About.[hash].js) for this route
//   // which is lazy-loaded when the route is visited.
//   component: () => import('../views/AboutView.vue')
// },

import HomeView from '@/views/HomeView.vue';
import LoginView from '@/views/LoginView.vue';
import RegisterView from '@/views/RegisterView.vue';
import DashboardView from '@/views/DashboardView.vue';
import CampaignView from '@/views/CampaignView.vue';

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        { path: '/', name: 'home', component: HomeView },
        { path: '/login', name: 'login', component: LoginView },
        { path: '/register', name: 'register', component: RegisterView },
        { path: '/dashboard', name: 'dashboard', component: DashboardView },
        { path: '/campaign/:id', name: 'campaign', component: CampaignView },
    ]
});

router.beforeEach((to, from, next) => {
    const isAuthenticated = sessionStorage.getItem('authToken');

    if (to.path === '/dashboard' && !isAuthenticated) {
        next('/login');
    } else {
        next();
    }
});

export default router
