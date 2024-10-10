import { useUserStore } from '@/stores/user';
import { useRouter } from 'vue-router';

const userLoggedInRedirect = () => {
    const store = useUserStore();
    const router = useRouter();
    if (store.getAuthToken) {
        router.push('/');
        return true;
    }
}

function clearCookie(cookieName) {
    console.log(`Cookie: ${cookieName} is cleared!`);
    document.cookie = cookieName + '=; Max-Age=-99999999;';
}


export { userLoggedInRedirect, clearCookie };
