<script setup>
import { formatNumber, redirectToErrorPage } from '@/utils';
import { onMounted, reactive, ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const searchForm = reactive({
    min_reach: null,
    category_id: '',
    niche: null,
});

const searchResults = ref([]);
const influencerCategories = ref([]);
const searched = ref(false);
const canAssignAd = ref(true);

const searchInfluencers = async () => {
    console.log('Search influencers.');
    try {
        const res = await fetch('/api/search/influencers', {
            method: 'POST',
            headers: {
                'Authentication-Token': localStorage.getItem('authToken'), 
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                min_reach: searchForm.min_reach,
                category_id: searchForm.category_id,
                niche: searchForm.niche
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
    searchForm.min_reach = null
    searchForm.category_id = ''
    searchForm.niche = null
    // searchInfluencers();
    searchResults.value = [];
    searched.value = false;
}

onMounted(async () => {
    try {
        const res = await fetch('/api/hard-coded-form-data');
        const data = await res.json();
        console.log(data.influencer_category_names);

        const fetchedInfluencerCategories = [];
        for (const [idx, categoryName] of data.influencer_category_names.entries()) {
            fetchedInfluencerCategories.push({ id: idx + 1, name: categoryName });
        }
        influencerCategories.value = [...fetchedInfluencerCategories];
    } catch (error) {
        console.error('Error fetching hard-coded data.', error);
    }

    // Check if an unassigned ad request can be assigned. 
    // If none exist, allow only to create an ad.
    try {
        const res = await fetch('/api/sponsor/campaigns', {
            method: 'GET',
            headers: { 'Authentication-Token': localStorage.getItem('authToken') }
        });

        if (!res.ok) {
            return redirectToErrorPage(res.status, router);
        }

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
                console.log('No campaigns with unassigned ads.');
                canAssignAd.value = false;
            }
        }
    } catch (error) {
        console.error('Error in fetching all campaigns of user.', error);
    }
});
</script>

<template>
    <h2 class="text-center mb-3 pt-2">Search for Influencers</h2>

    <div class="row my-4 justify-content-center">
        <div class="col-md-6">
            <form @submit.prevent="searchInfluencers" class="p-4 border rounded shadow-sm">
                <div class="mb-3">
                    <label for="min_reach" class="form-label">Reach <span>&#8805;</span></label>
                    <input v-model="searchForm.min_reach" class="form-control" type="number" name="min_reach" id="min_reach" aria-describedby="min-reach" min="0" step="10000">
                    <div id="min-reach" class="form-text">Minimum reach of influencer.</div>
                </div>
                <div class="mb-3">
                    <label for="category" class="form-label">Influencer Category</label>
                    <select v-model="searchForm.category_id" name="category_id" id="category" class="form-select">
                        <option value="" selected>All Categories</option>
                        <option v-for="category in influencerCategories" :value="category.id">{{ category.name }}</option>
                    </select>
                </div>
                <div class="mb-3">
                    <label for="niche" class="form-label">Niche Keyword</label>
                    <input v-model="searchForm.niche" class="form-control" type="text" name="niche" id="niche" aria-describedby="niche-keyword">
                    <div id="niche-keyword" class="form-text">Specify a niche keyword.</div>
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
            v-for="influencer in searchResults" 
            :key="influencer.id" 
            class="col-md-4 mb-4"
        >
            <div class="card shadow-sm h-100">
                <div class="card-body d-flex flex-column">
                    <h3 class="card-title">{{ influencer.name }}</h3>

                    <ul class="list-unstyled">
                        <li>
                            <strong>Category:</strong> {{ influencer.category }}
                        </li>
                        <li>
                            <strong>Niche: </strong>
                            <span 
                                class="badge badge-pill bg-dark me-1" 
                                v-for="tag in influencer.niche.split(', ').slice(0, 2)"
                            >
                                {{ tag }}
                            </span>
                        </li>
                        <li>
                            <strong>Reach:</strong> {{ formatNumber(influencer.reach) }} people
                        </li>
                    </ul>

                    <div class="d-flex gap-2 mt-auto">
                        <RouterLink 
                            :to="`/ad-request/assign?influencer_id=${influencer.id}`" 
                            class="btn btn-outline-primary btn-sm" 
                            v-if="canAssignAd"
                        >
                            Assign Ad
                        </RouterLink>
                        <RouterLink 
                            :to="`/ad-request/create?influencer_id=${influencer.id}`" 
                            class="btn btn-outline-success btn-sm"
                        >
                            Create Ad
                        </RouterLink>
                    </div>
                </div>
            </div>
        </div>
        <p v-if="searchResults.length == 0 && searched" class="text-center">
            No influencers found.
        </p>
    </div>
</template>
