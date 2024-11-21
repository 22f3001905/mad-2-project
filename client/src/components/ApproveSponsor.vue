<script setup>
import { onMounted, reactive } from 'vue';
import { redirectToErrorPage } from '@/utils';
import { useRouter } from 'vue-router';

const router = useRouter();

const state = reactive({
    sponsors: []
});

const approveSponsor = async (sponsor_id) => {
    try {
        const res = await fetch(`/api/sponsor-approval/${sponsor_id}`, {
            headers: { 'Authentication-Token': localStorage.getItem('authToken') }
        });

        if (!res.ok) {
            return redirectToErrorPage(res.status, router);
        }

        const data = await res.json();
        console.log(data);
        state.sponsors = state.sponsors.filter(sponsor => sponsor.id != sponsor_id);
    } catch (error) {
        console.error('Sponsor approval unsuccessful.', error);
    }
}

onMounted(async () => {
    try {
        const res = await fetch('/api/sponsors-approval-pending', {
            headers: { 'Authentication-Token': localStorage.getItem('authToken') }
        });

        if (!res.ok) {
            return redirectToErrorPage(res.status, router);
        }

        const data = await res.json();
        state.sponsors = state.sponsors.concat(data.data);
        console.log(data.data);
    } catch (error) {
        console.error('Could not fetch unapproved sponsors.', error);
    }
});
</script>

<template>
    <div class="pt-2">
        <h2 class="mb-4">Approve Sponsor Registration</h2>
        <div class="row">
            <div 
                v-for="sponsor in state.sponsors" 
                :key="sponsor.id"
                class="col-md-4 mb-4"
            >
                <div class="card shadow-sm h-100">
                    <div class="card-body d-flex flex-column">
                        <h3 class="card-title">{{ sponsor.name }}</h3>
                        <ul class="list-unstyled">
                            <li>
                                <strong>Email:</strong> {{ sponsor.email }}
                            </li>
                            <li>
                                <strong>Industry:</strong> {{ sponsor.industry }}
                            </li>
                        </ul>
                        <div class="mt-auto">
                            <button 
                                @click="approveSponsor(sponsor.id)" 
                                class="btn btn-success btn-sm"
                            >Approve</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <p v-if="state.sponsors.length == 0">
            No sponsors on the approval waiting list.
        </p>
    </div>
</template>
