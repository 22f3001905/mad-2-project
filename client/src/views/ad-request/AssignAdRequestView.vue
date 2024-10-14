<script setup>
import Navbar from '@/components/Navbar.vue';
import { onMounted, reactive, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();

const influencerId = ref(route.query.influencer_id || null);
const influencerName = ref('influencer_name');

if (!influencerId.value) {
    router.push('/search');
}

const state = reactive({
    campaigns: [],
    adRequests: []
});

const form = reactive({
    campaign_id: null,
    ad_request_id: null
});

// TODO: Help me!
const changeSelectedCampaign = async () => {
    console.log('campaign changed.');
	state.adRequests = [];
    try {
        const res = await fetch(`/api/campaign/${form.campaign_id}`, {
            headers: { 'Authentication-Token': localStorage.getItem('authToken') }
        });
        const data = await res.json();
        // console.log(data);
        const validAds = [];
        for (const ad of data.ad_requests) {
            if (ad.influencer.id == null) {
                validAds.push(ad);
            }
        }
        if (validAds.length == 0) {
            router.push('/campaigns');
        }
        state.adRequests = validAds;
        form.ad_request_id = state.adRequests[0].id;
    } catch (error) {
        console.error('Error fetching ad requests for a campaign.', error);
    }
}

// TODO
const assignAd = async () => {
    console.log('assign ass.');
    try {
        const res = await fetch('/api/assign-ad', {
            method: 'POST',
            headers: {
                'Authentication-Token': localStorage.getItem('authToken'),
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                ad_request_id: form.ad_request_id,
                influencer_id: influencerId.value
            })
        })
        const data = await res.json()
        console.log(data);
        router.push('/search');
    } catch (error) {
        console.error('Error in assigning ad.', error);
    }
}

onMounted(async () => {
    try {
        const res = await fetch('/api/sponsor/campaigns', {
            method: 'GET',
            headers: { 'Authentication-Token': localStorage.getItem('authToken') }
        });
        const data = await res.json();
        console.log(data.campaigns);
        const validCampaigns = [];  // Campaigns with unassigned ads.
        if (data.campaigns) {
            for (const camp of data.campaigns) {
                if (camp.n_unassigned_ads) {
                    validCampaigns.push(camp);
                }
            }
            if (validCampaigns.length == 0) {
                router.push('/campaigns');
            }
            state.campaigns = [...validCampaigns];
            form.campaign_id = state.campaigns[0].id;
        } else {
            router.push('/campaign/create');
        }
    } catch (error) {
        console.error('Error fetching all the campaigns for this user.', error);
    }

    try {
        const res = await fetch(`/api/influencer/${influencerId.value}`);
        const data = await res.json();
        influencerName.value = data.influencer.name;
    } catch (error) {
        console.error('Error fetching influencer details.', error);
    }

    try {
        const res = await fetch(`/api/campaign/${form.campaign_id}`, {
            headers: { 'Authentication-Token': localStorage.getItem('authToken') }
        });
        const data = await res.json();
        // console.log('hehehehehe', data);
        const validAds = [];
        for (const ad of data.ad_requests) {
            if (ad.influencer.id == null) {
                validAds.push(ad);
            }
        }
        if (validAds.length == 0) {
            router.push('/campaigns');
        }
        state.adRequests = validAds;
        form.ad_request_id = state.adRequests[0].id;
    } catch (error) {
        console.error('Error fetching ad requests for a campaign.', error);
    }
});
</script>

<template>
    <Navbar />
    <h1 class="text-center mb-3">Assign Ad Request</h1>
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="mb-3">Target Influencer: {{ influencerName }}</div>
            <form @submit.prevent="assignAd">
                <div class="mb-3">
                    <label for="campaign_id" class="form-label">Campaign</label>
                    <select v-model="form.campaign_id" name="campaign_id" id="campaign_id" class="form-select" @change="changeSelectedCampaign" required>
                        <option v-for="campaign in state.campaigns" :value="campaign.id">
                            {{ campaign.name }} {{ campaign.visibility == 'Private' ? '(Private)' : '' }}
                        </option>
                    </select>
                </div>
                <div class="mb-3">
                    <label for="ad_request_id" class="form-label">Ad Request Requirement</label>
                    <select v-model="form.ad_request_id" name="ad_request_id" id="ad_request_id" class="form-select" required>
                        <option v-for="ad in state.adRequests" :value="ad.id">{{ ad.requirement }}</option>
                    </select>
                </div>
                <div>
                    <button type="submit" class="btn btn-primary">Assign Ad Request</button>
                </div>
            </form>
        </div>
    </div>
</template>
