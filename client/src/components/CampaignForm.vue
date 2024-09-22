<script setup>
import { defineProps, reactive, ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const props = defineProps({
    title: String,  // 'Create' or 'Edit'
    budget: Number
});

const form = reactive({
    name: '',
    description: '',
    niche_id: 1,
    start_date: null,
    end_date: null,
    budget: null,
    visibility_id: 1,
    goals: ''
});

const route = useRoute();
const campaignNiches = ref([]);
const campaignId = ref(route.params.id);

onMounted(async () => {
    try {
        const response = await fetch('/api/hard-coded-form-data');
        const data = await response.json();
        const fetchedCampaignNiches = [];
        for (const [idx, campaignNiche] of data.campaign_niche_names.entries()) {
            fetchedCampaignNiches.push({ id: idx + 1, name: campaignNiche })
        }
        campaignNiches.value = [...fetchedCampaignNiches];
    } catch (error) {
        console.error('Error fetching hard coded form data.', error);
    }
    if (props.title == 'Edit') {
        try {
            const res = await fetch(`/api/campaign/${campaignId.value}`, {
                method: 'GET',
                headers: { 'Authentication-Token': sessionStorage.getItem('authToken') }
            });
            const data = await res.json();
            console.log(data);

            form.name = data.name;
            form.description = data.description;
            form.start_date = data.start_date;
            form.end_date = data.end_date;
            form.budget = data.budget;
            form.niche_id = data.niche.id;
            form.visibility_id = data.visibility.id;
            // form.goals = data.goals;
        } catch (error) {
            console.error('Error in fetching campaign data.', error);
        }
    }
});

const createCampaign = async () => {
    console.log(form);
}
const editCampaign = async () => {
    console.log(form);
}
</script>

<template>
    <h1>{{ title }} Campaign</h1>
    <form @submit.prevent="props.title == 'Create' ? createCampaign : editCampaign">
        <div class="mb-3">
            <label for="name" class="form-label">Campaign Name</label>
            <input v-model="form.name" class="form-control" type="text" name="name" id="name" required>
        </div>
        <div class="mb-3">
            <label for="description" class="form-label">Description</label>
            <input v-model="form.description" class="form-control" type="text" name="description" id="description" required placeholder="Describe your campaign." maxlength="200">
        </div>
        <div class="mb-3">
            <label for="niche" class="form-label">Niche</label>
            <select v-model="form.niche_id" name="niche_id" id="niche" class="form-select" required>
                <option v-for="campaignNiche in campaignNiches" :value="campaignNiche.id" :key="campaignNiche.id">{{ campaignNiche.name }}</option>
            </select>
        </div>
        <div class="row">
            <div class="mb-3 col">
                <label for="start_date" class="form-label">Start Date</label>
                <input v-model="form.start_date" class="form-control" type="date" name="start_date" id="start_date" required>
            </div>
            <div class="mb-3 col">
                <label for="end_date" class="form-label">End Date</label>
                <input v-model="form.end_date" class="form-control" type="date" name="end_date" id="end_date" required>
            </div>
        </div>
        <div class="mb-3">
            <label for="budget" class="form-label">Budget</label>
            <input v-model="form.budget" class="form-control" type="number" name="budget" id="budget" required
                aria-describedby="payment-budget" :max="budget" min="0">
            <div id="payment-budget" class="form-text">Remaining Sponsor Budget: Rs. {{ budget }}</div>
        </div>
        <div class="mb-3">
            <label for="visibility" class="form-label">Visibility</label>
            <select v-model="form.visibility_id" name="visibility_id" id="visibility" class="form-select" required>
                <option value="1">Public</option>
                <option value="2">Private</option>
            </select>
        </div>
        <div class="mb-3" v-if="props.title == 'Create'">
            <label for="goals" class="form-label">Goals</label>
            <textarea v-model="form.goals" class="form-control" type="text" name="goals" id="goals" required aria-describedby="campaign-goals" maxlength="200"></textarea>
            <div id="campaign-goals" class="form-text">Write each goal on a new line.</div>
        </div>
        <div class="mb-5">
            <button type="submit" class="btn btn-primary">{{ title }} Campaign</button>
        </div>
    </form>
</template>
