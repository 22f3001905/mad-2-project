<script setup>
import { onMounted, reactive } from 'vue';
import Navbar from '@/components/Navbar.vue';
import { formatNumber, redirectToErrorPage } from '@/utils';
import { useRouter } from 'vue-router';

const router = useRouter();

const form = reactive({
    money: null,
});

const sponsor = reactive({
    id: null,
    budget: 0,
})

async function addMoney() {
    console.log('Add money.', form.money);

    try {
        const res = await fetch(`/api/add-money`, {
            method: 'POST',
            headers: {
                'Authentication-Token': localStorage.getItem('authToken'), 
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                amount: form.money,
            })
        });

        if (!res.ok) {
            return redirectToErrorPage(res.status, router);
        }

        const data = await res.json();
        console.log(data);

        return router.push('/dashboard');
    } catch (error) {
        console.error('Error in adding money to sponsor account.', error);
    }
}

onMounted(async () => {
    try {
        const res = await fetch('/api/sponsor-budget', {
            headers: {
                'Authentication-Token': localStorage.getItem('authToken')
            }
        });

        if (!res.ok) {
            return redirectToErrorPage(res.status, router);
        }

        const data = await res.json();
        console.log(data);
        sponsor.budget = data.budget;
    } catch (error) {
        console.error('Error fetching sponsor budget.', error);
    }
});
</script>

<template>
    <Navbar />
    <h2 class="text-center mb-3 pt-2">Ad Request</h2>
    <div class="row justify-content-center">
        <div class="col-md-6">
            <form
                @submit.prevent="addMoney" 
                class="p-4 border rounded shadow-sm"
            >
                <div class="mb-3">
                    <label for="money" class="form-label">Amount</label>
                    <input 
                        v-model="form.money" 
                        class="form-control" 
                        type="number" 
                        name="money" 
                        id="money" 
                        required 
                        min="0" 
                        step="100" 
                        aria-describedby="sponsor-budget" 
                    />
                    <div id="sponsor-budget" class="form-text">
                        Added to your Wallet Balance of Rs. {{ formatNumber(sponsor.budget) }}
                    </div>
                </div>
                <div>
                    <button type="submit" class="btn btn-primary">
                        Add
                    </button>
                </div>
            </form>
        </div>
    </div>
</template>
