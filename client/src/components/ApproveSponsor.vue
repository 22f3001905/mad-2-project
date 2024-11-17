<script setup>
import { onMounted, reactive } from 'vue';

const state = reactive({
    sponsors: []
});

const approveSponsor = async (sponsor_id) => {
    try {
        const res = await fetch(`/api/sponsor-approval/${sponsor_id}`, {
            headers: { 'Authentication-Token': localStorage.getItem('authToken') }
        });
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
        const data = await res.json();
        state.sponsors = state.sponsors.concat(data.data);
    } catch (error) {
        console.error('Could not fetch unapproved sponsors.', error);
    }
});
</script>

<template>
    <div>
        <h2>Approve Sponsor Registration</h2>
        <ul>
            <li v-for="sponsor in state.sponsors">{{ sponsor.name }} | Email: {{ sponsor.email }} | <button @click="approveSponsor(sponsor.id)">Approve</button></li>
        </ul>
        <p v-if="state.sponsors.length == 0">No more sponsors on the approval list.</p>
    </div>
</template>
