<script setup>
import { defineProps, reactive, onMounted, ref } from 'vue';
import { useRouter, useRoute } from 'vue-router'; 

const route = useRoute();
const router = useRouter();

const props = defineProps({
    title: String
});

const influencerId = ref(route.query.influencer_id || null);
const influencerName = ref('influencer_name');

const form = reactive({
    requirement: '',
    message: '',
    newMessage: '',
    payment_amount: null,
    campaign_goal_id: null,
    sender_user_id: JSON.parse(localStorage.getItem('user')).id,
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
    // fetch campaign goals
    if (props.title != 'Negotiate') {
        try {
            const res = await fetch('/api/sponsor/campaigns', {
                method: 'GET',
                headers: { 'Authentication-Token': localStorage.getItem('authToken') }
            });
            const data = await res.json();
            console.log(data.campaigns);
            state.campaigns = [...data.campaigns];

            if (data.campaigns.length) {
                // By defeault select the first campaign.
                let campaign = null;
                if (route.query.campaign_id) {
                    campaign = data.campaigns.filter(camp => camp.id == route.query.campaign_id)[0]
                } else {
                    campaign = data.campaigns[0];
                }

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
    }

    if (props.title == 'Edit') {
        const adRequestId = ref(route.params.id);
        try {
            const res = await fetch(`/api/ad-request/${adRequestId.value}`, {
                method: 'GET',
                headers: { 'Authentication-Token': localStorage.getItem('authToken') }
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
            console.error('Error fetching ad request data.', error);
        }
    }

    if (props.title == 'Negotiate') {
        const adRequestId = ref(route.params.id);
        try {
            const res = await fetch(`/api/ad-request/${adRequestId.value}`, {
                method: 'GET',
                headers: { 'Authentication-Token': localStorage.getItem('authToken') }
            });
            const data = await res.json();
            console.log(data);

            form.campaign.id = data.campaign_id;

            try {
                const r = await fetch(`/api/campaign/${data.campaign_id}`, {
                    method: 'GET',
                    headers: { 'Authentication-Token': localStorage.getItem('authToken') }
                });

                const d = await r.json();
                console.log(d);
                state.campaignBudget = d.budget + data.payment_amount;
            } catch (error) {
                console.error('Error fetching campaign data.', error);
            }

            form.requirement = data.requirement;
            form.message = data.message;
            form.payment_amount = data.payment_amount;
            // form.sender_user_id = data.sender_user_id;
        } catch (error) {
            console.error('Error fetching ad request data.', error);
        }
    }

    if (influencerId.value) {
        console.log('Fetch influencer name.');
        try {
            const res = await fetch(`/api/influencer/${influencerId.value}`);
            const data = await res.json();
            influencerName.value = data.influencer.name;
        } catch (error) {
            console.error('Error fetching influencer details.', error);
        }
    }
});

const createAdRequest = async () => {
    console.log(form);
    try {
        const res = await fetch(`/api/ad-request`, {
            method: 'POST',
            headers: {
                'Authentication-Token': localStorage.getItem('authToken'), 
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                campaign_id: form.campaign.id,
                influencer_id: influencerId.value,
                requirement: form.requirement,
                message: form.message,
                payment_amount: form.payment_amount,
                status_id: 1,
                sender_user_id: form.sender_user_id,
                campaign_goal_id: form.campaign_goal_id
            })
        });
        const data = await res.json();
        console.log(data);
        router.push(`/campaign/${form.campaign.id}`);
    } catch (error) {
        console.error('Error posting ad request data.', error);
    }
}

const editAdRequest = async () => {
    try {
        const adRequestId = ref(route.params.id);
        const res = await fetch(`/api/ad-request/${adRequestId.value}`, {
            method: 'PUT',
            headers: {
                'Authentication-Token': localStorage.getItem('authToken'), 
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                campaign_id: form.campaign.id,
                influencer_id: influencerId.value,
                requirement: form.requirement,
                message: form.message,
                payment_amount: form.payment_amount,
                sender_user_id: form.sender_user_id,
                campaign_goal_id: form.campaign_goal_id
            })
        });
        const data = await res.json();
        console.log(data);
        router.push(`/campaign/${data.campaign_id}`);
    } catch (error) {
        console.error('Error in editing ad request data.', error);
    }
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

const negotiateAdRequest = async () => {
    const adRequestId = ref(route.params.id);
    console.log('Negotiate');
    try {
        const res = await fetch(`/api/ad-request/${adRequestId.value}/negotiate`, {
            method: 'POST',
            headers: {
                'Authentication-Token': localStorage.getItem('authToken'), 
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                payment_amount: form.payment_amount,
                message: form.newMessage,
                requirement: form.requirement,
                // sender_user_id: form.sender_user_id
            })
        });
        const data = await res.json();
        console.log(data);
    } catch (error) {
        console.error('Error posting form data for negotiation of ad request.', error);
    }
}

function submitForm() {
    if (props.title === 'Create') {
        return createAdRequest();
    } else if (props.title === 'Edit') {
        return editAdRequest();
    } else {
        return negotiateAdRequest();
    }
}

</script>

<template>
    <h1 class="text-center mb-3">{{ props.title }} Ad Request</h1>
    <div class="row justify-content-center">
        <div class="col-md-6">
            <p v-if="influencerId">Target Influencer: {{ influencerName }}</p>
            <form @submit.prevent="submitForm">
                <div class="mb-3" v-if="props.title != 'Negotiate'">
                    <label for="campaign">Campaign</label>
                    <select v-model="form.campaign.id" name="campaign" id="campaign" @change="changeSelectedCampaign" :disabled="props.title == 'Edit'">
                        <option v-for="campaign in state.campaigns" :value="campaign.id">
                            {{ campaign.name }} {{ campaign.visibility == 'Private' ? '(Private)' : '' }}
                        </option>
                    </select>
                </div>
                <div class="mb-3" v-if="props.title != 'Negotiate'">
                    <label for="goal_id" class="form-label">Target Goal</label>
                    <select v-model="form.campaign_goal_id" name="goal_id" id="goal_id" class="form-select" required>
                        <option v-if="!form.campaign">Campaign Goal</option>
                        <option v-else v-for="goal in form.campaign.goals" :value="goal.id">
                            {{ goal.name }}
                        </option>
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
                <div class="mb-3" v-if="props.title != 'Negotiate'">
                    <label for="message" class="form-label">Message</label>
                    <input v-model="form.message" class="form-control" type="text" name="message" id="message" required>
                </div>
                <div class="mb-3" v-else>
                    <p>Previous Message<br>{{ form.message }}</p>
                    <label for="message" class="form-label">New Message</label>
                    <input v-model="form.newMessage" class="form-control" type="text" name="message" id="message" required>
                </div>
                <div>
                    <button type="submit" class="btn btn-primary">{{ props.title }} Ad Request</button>
                </div>
            </form>
        </div>
    </div>
</template>
