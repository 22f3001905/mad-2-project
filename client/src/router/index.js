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
import CampaignView from '@/views//campaign/CampaignView.vue';
import CreateCampaignView from '@/views/campaign/CreateCampaignView.vue';
import EditCampaignView from '@/views/campaign/EditCampaignView.vue';
import AllCampaignsView from '@/views/campaign/AllCampaignsView.vue';
import CreateAdRequestView from '@/views/ad-request/CreateAdRequestView.vue';
import EditAdRequestView from '@/views/ad-request/EditAdRequestView.vue';
import SearchView from '@/views/SearchView.vue';
import AssignAdRequestView from '@/views/ad-request/AssignAdRequestView.vue';
import NegotiateAdRequestView from '@/views/ad-request/NegotiateAdRequestView.vue';
import AdvertsView from '@/views/AdvertsView.vue';
import StatsView from '@/views/StatsView.vue';
import UserView from '@/views/UserView.vue';
import AboutView from '@/views/AboutView.vue';
import ErrorView from '@/views/ErrorView.vue';
import AddMoneyView from '@/views/AddMoneyView.vue';
import InfluencerProfileView from '@/views/InfluencerProfileView.vue';

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        { path: '/', name: 'home', component: HomeView },
        { path: '/login', name: 'login', component: LoginView },
        { path: '/register', name: 'register', component: RegisterView },
        { path: '/dashboard', name: 'dashboard', component: DashboardView },
        { path: '/campaigns', name: 'all-campaign', component: AllCampaignsView },
        { path: '/campaign/:id', name: 'campaign', component: CampaignView },
        { path: '/campaign/:id/edit', name: 'edit-campaign', component: EditCampaignView },
        { path: '/campaign/create', name: 'create-campaign', component: CreateCampaignView },
        { path: '/ad-request/create', name: 'create-ad', component: CreateAdRequestView },
        { path: '/ad-request/:id/edit', name: 'edit-ad', component: EditAdRequestView },
        { path: '/ad-request/assign', name: 'assign-ad', component: AssignAdRequestView },
        { path: '/search', name: 'search', component: SearchView },
        { path: '/ad-request/:id/negotiate', name: 'negotiate-ad', component: NegotiateAdRequestView },
        { path: '/adverts', name: 'adverts', component: AdvertsView },
        { path: '/stats', name: 'user-stats', component: StatsView },
        { path: '/user/:id', name: 'user-profile', component: UserView },
        { path: '/influencer/:id', name: 'influencer-profile', component: InfluencerProfileView },
        { path: '/about', name: 'about', component: AboutView },
        { path: '/add-money', name: 'add-money', component: AddMoneyView },
        { path: '/403', name: 'permission-denied', component: ErrorView, props: { statusCode: 403, description: 'You do not have permission to access this page.' } },
        { path: '/404', name: 'not-found', component: ErrorView, props: { statusCode: 404, description: 'The page you are looking for does not exist.' } },
        { path: '/500', name: 'internal-error', component: ErrorView, props: { statusCode: 500, description: 'Internal Server Error. Please try again later.' } },
        { path: '/error', name: 'error', component: ErrorView },
        // { path: '/:catchAll(.*)', redirect: '/404' },
    ]
});

router.beforeEach((to, from, next) => {
    const isAuthenticated = localStorage.getItem('authToken');

    if (to.path === '/dashboard' && !isAuthenticated) {
        next('/login');
    } else {
        next();
    }
});

export default router
