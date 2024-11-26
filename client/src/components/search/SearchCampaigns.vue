<script setup>
import { formatNumber, redirectToErrorPage } from '@/utils';
import { onMounted, reactive, ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const searchForm = reactive({
    min_budget: null,
    niche_id: '',
    keyword: null,
});

const searchResults = ref([]);
const searched = ref(false);

const searchCampaigns = async () => {
    try {
        const res = await fetch('/api/search/campaigns', {
            method: 'POST',
            headers: {
                'Authentication-Token': localStorage.getItem('authToken'), 
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                min_budget: searchForm.min_budget,
                niche_id: searchForm.niche_id,
                keyword: searchForm.keyword
            })
        });

        if (!res.ok) {
            return redirectToErrorPage(res.status, router);
        }

        const data = await res.json();
        console.log(data);
        searchResults.value = [...data.data];
        searched.value = true;
    } catch (error) {
        console.error('Error in fetching search influencers results.', error);
    }
}

const resetSearch = () => {
    searchForm.min_budget = null;
    searchForm.niche_id = '';
    searchForm.keyword = null;
    searchResults.value = [];
    searched.value = false;
}

const campaignNiches = ref([]);

onMounted(async () => {
    try {
        const res = await fetch('/api/hard-coded-form-data');

        if (!res.ok) {
            return redirectToErrorPage(res.status, router);
        }

        const data = await res.json();
        console.log(data.campaign_niche_names);

        const fetchedCampaignNiches = [];
        for (const [idx, campaignNiche] of data.campaign_niche_names.entries()) {
            fetchedCampaignNiches.push({ id: idx + 1, name: campaignNiche })
        }
        campaignNiches.value = [...fetchedCampaignNiches];
    } catch (error) {
        console.error('Error fetching hard-coded data.', error);
    }
});
</script>

<template>
    <h2 class="text-center mb-3 pt-2">Search for Campaigns</h2>

    <div class="row my-4 justify-content-center">
        <div class="col-md-6">
            <form @submit.prevent="searchCampaigns" class="p-4 border rounded shadow-sm">
                <div class="mb-3">
                    <label for="min_budget" class="form-label">Campaign Budget <span>&#8805;</span></label>
                    <input v-model="searchForm.min_budget" class="form-control" type="number" name="min_budget" id="min_budget" aria-describedby="min-budget" min="0" step="1000">
                    <div id="min-budget" class="form-text">Minimum Budget.</div>
                </div>

                <div class="mb-3">
                    <label for="niche" class="form-label">Campaign Niche</label>
                    <select v-model="searchForm.niche_id" name="niche_id" id="niche" class="form-select">
                        <option value="" selected>All Niches</option>
                        <option v-for="niche in campaignNiches" :value="niche.id">{{ niche.name }}</option>
                    </select>
                </div>

                <div class="mb-3">
                    <label for="keyword" class="form-label">Search Keyword</label>
                    <input v-model="searchForm.keyword" class="form-control" type="text" name="keyword" id="keyword" aria-describedby="search-keyword">
                    <div id="search-keyword" class="form-text">Specify a Campaign search keyword.</div>
                </div>

                <div class="d-flex justify-content-start gap-2 mt-4">
                    <button type="submit" class="btn btn-outline-primary">
                        Search
                    </button>
                    <button
                        id="reset"
                        type="button"
                        class="btn btn-outline-dark"
                        @click="resetSearch"
                    >
                        Reset
                    </button>
                </div>
            </form>
        </div>
    </div>

    <div class="row my-4">
        <div 
            v-for="campaign in searchResults" 
            :key="campaign.id" 
            class="col-md-4 mb-4"
        >
            <div class="card shadow-sm h-100">
                <div class="card-body d-flex flex-column">
                    <h3 class="card-title">{{ campaign.name }}</h3>
                    <p class="card-text text-muted">{{ campaign.description }}</p>

                    <ul class="list-unstyled">
                        <li>
                            <strong>Sponsor:</strong> {{ campaign.sponsor }}
                        </li>
                    </ul>

                    <ul class="list-unstyled">
                        <li>
                            <strong>Starts:</strong> {{ new Date(campaign.start_date).toDateString() }}
                        </li>
                        <li>
                            <strong>Ends:</strong> {{ new Date(campaign.end_date).toDateString() }}
                        </li>
                    </ul>

                    <ul class="list-unstyled">
                        <li>
                            <strong>Visibility:</strong> {{ campaign.visibility }}
                        </li>
                        <li>
                            <strong>Budget:</strong> Rs. {{ formatNumber(campaign.budget) }}
                        </li>
                        <li>
                            <strong>Niche:</strong> {{ campaign.niche }}
                        </li>
                    </ul>

                    <div class="mt-auto">
                        <RouterLink 
                            :to="`/campaign/${campaign.id}`" 
                            class="btn btn-primary btn-sm"
                        >
                            View
                        </RouterLink>
                    </div>
                </div>
            </div>
        </div>
        <p v-if="searchResults.length == 0 && searched" class="text-center">
            No campaigns found.
        </p>
    </div>
</template>
