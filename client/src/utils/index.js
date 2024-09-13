import { useUserStore } from '@/stores/user';
import { useRouter } from 'vue-router';

const userLoggedInRedirect = () => {
    const store = useUserStore();
    const router = useRouter();
    if (store.isLoggedIn) {
        router.push('/');
    }
}

export { userLoggedInRedirect };
