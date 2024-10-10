<script setup>
import { onMounted, reactive, ref } from 'vue';

const searchForm = reactive({
    min_budget: null,
    niche_id: '',
    keyword: null,
});

const searchResults = ref([]);

const searchCampaigns = async () => {
    console.log('Search campaigns.');
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
        const data = await res.json();
        console.log(data);
        searchResults.value = [...data.data];
    } catch (error) {
        console.error('Error in fetching search influencers results.', error);
    }
}

const resetSearch = () => {
    searchForm.min_budget = null;
    searchForm.niche_id = '';
    searchForm.keyword = null;
    searchResults.value = [];
}

const campaignNiches = ref([]);

onMounted(async () => {
    try {
        const res = await fetch('/api/hard-coded-form-data');
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
    <h2>Search for Campaigns</h2>
    <form @submit.prevent="searchCampaigns">
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
        <div>
            <button type="submit" class="btn btn-primary">Refine Search</button>
            <button id="reset" type="button" class="btn btn-warning" @click="resetSearch">Reset</button>
        </div>
    </form>
    <div>
        <div v-for="campaign in searchResults">{{ campaign.name }}</div>
    </div>
</template>
