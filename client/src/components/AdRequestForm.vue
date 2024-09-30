<script setup>
import { defineProps, reactive, onMounted, ref } from 'vue';
import { useRouter, useRoute } from 'vue-router'; 

const route = useRoute();
const router = useRouter();

const props = defineProps({
    title: String
});

const form = reactive({
    requirement: '',
    message: '',
    payment_amount: null,
    campaign_goal_id: null,
    sender_user_id: null,
    campaign: {
        id: null,
        // name: null,
        flagged: null,
        goals: []
    },
});

const state = reactive({
    // default 1st campign, if none redirect to create campaign page.
    campaigns: [],
    campaignBudget: 0
});

onMounted(async () => {
    // fetch sponsor goals
    try {
        const res = await fetch('/api/all-campaigns', {
            method: 'GET',
            headers: { 'Authentication-Token': sessionStorage.getItem('authToken') }
        });
        const data = await res.json();
        console.log(data.campaigns);
        state.campaigns = [...data.campaigns];

        if (data.campaigns.length) {
            const campaign = data.campaigns[0];

            form.campaign.id = campaign.id;
            // form.campaign.name = campaign.name;
            form.campaign.flagged = campaign.flagged;
            form.campaign.goals = [...campaign.goals];
            form.campaign_goal_id = campaign.goals[0].id;
            
            state.campaignBudget = campaign.budget;
        } else {
            console.log('No campaigns created yet!');
            router.push('/campaign/create');
        }
    } catch (error) {
        console.error('Error fetching all the campaigns for this user.', error);
    }

    if (props.title == 'Edit') {
        const adRequestId = ref(route.params.id);
        try {
            const res = await fetch(`/api/ad-request/${adRequestId.value}`, {
                method: 'GET',
                headers: { 'Authentication-Token': sessionStorage.getItem('authToken') }
            });
            const data = await res.json();
            console.log(data);

            form.campaign.id = data.campaign_id;
            const selectedCampaign = state.campaigns.filter(camp => camp.id ==  form.campaign.id)[0];
            form.campaign.flagged = selectedCampaign.flagged;
            form.campaign.goals = [...selectedCampaign.goals];

            form.requirement = data.requirement;
            form.message = data.message;
            form.payment_amount = data.payment_amount;
            form.campaign_goal_id = data.campaign_goal_id;
            form.sender_user_id = data.sender_user_id;

            state.campaignBudget = selectedCampaign.budget + data.payment_amount;
        } catch (error) {
            console.error('Error fetching Ad request data.', error);
        }
    }
});

const createAdRequest = async () => {
    console.log(form);
}

const changeSelectedCampaign = () => {
    const selectedCampaign = state.campaigns.filter(camp => camp.id ==  form.campaign.id)[0];

    console.log(selectedCampaign);

    // form.campaign.name = selectedCampaign.name;
    form.campaign.flagged = selectedCampaign.flagged;
    form.campaign.goals = [...selectedCampaign.goals];
    form.campaign_goal_id = selectedCampaign.goals[0].id;

    state.campaignBudget = selectedCampaign.budget;
}
</script>

<template>
    <h1 class="text-center mb-3">{{ props.title }} Ad Request</h1>
    <div class="row justify-content-center">
        <div class="col-md-6">
            <form @submit.prevent="createAdRequest">
                <div class="mb-3">
                    <label for="campaign">Campaign</label>
                    <select v-model="form.campaign.id" name="campaign" id="campaign" @change="changeSelectedCampaign" :disabled="props.title == 'Edit'">
                        <option v-for="campaign in state.campaigns" :value="campaign.id">{{ campaign.name }}</option>
                    </select>
                </div>
                <div class="mb-3">
                    <label for="goal_id" class="form-label">Target Goal</label>
                    <select v-model="form.campaign_goal_id" name="goal_id" id="goal_id" class="form-select" required>
                        <option v-if="!form.campaign">Campaign Goal</option>
                        <option v-else v-for="goal in form.campaign.goals" :value="goal.id">{{ goal.name }}</option>
                    </select>
                </div>
                <div class="mb-3">
                    <label for="requirement" class="form-label">Requirement</label>
                    <input v-model="form.requirement" class="form-control" type="text" name="requirement" id="requirement" required>
                </div>
                <div class="mb-3">
                    <label for="payment_amount" class="form-label">Payment Amount</label>
                    <input v-model="form.payment_amount" class="form-control" type="number" name="payment_amount" id="payment_amount" required aria-describedby="payment-budget" min="0" :max="state.campaignBudget" step="100">
                    <div id="payment-budget" class="form-text">Remaining Campaign Budget: Rs. {{ state.campaignBudget }}</div>
                </div>
                <div class="mb-3">
                    <label for="message" class="form-label">Message</label>
                    <input v-model="form.message" class="form-control" type="text" name="message" id="message" required>
                </div>
                <div>
                    <button type="submit" class="btn btn-primary">Create Ad Request</button>
                </div>
            </form>
        </div>
    </div>
</template>
