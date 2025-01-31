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

function formatNumber(value) {
    return new Intl.NumberFormat().format(value);
}

function redirectToErrorPage(status, router) {
    if (status == 403) {
        return router.push('/403');
    } else if (status == 404) {
        return router.push('/404');
    } else if (status == 500) {
        return router.push('/500');
    } else {
        return router.push('/error');
    }
}


export { userLoggedInRedirect, clearCookie, formatNumber, redirectToErrorPage };
