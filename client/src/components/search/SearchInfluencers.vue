<script setup>
import { onMounted, reactive, ref } from 'vue';

const searchForm = reactive({
    min_reach: null,
    category_id: '',
    niche: null,
});

const searchResults = ref([]);
const influencerCategories = ref([]);

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
        const data = await res.json();
        console.log(data);
        searchResults.value = [...data.data];
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
});
</script>

<template>
    <h2>Search for Influencers</h2>
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
        <div>
            <button type="submit" class="btn btn-primary">Refine Search</button>
            <button id="reset" type="button" class="btn btn-warning" @click="resetSearch">Reset</button>
        </div>
    </form>
    <div v-if="searchResults.length">
        <h3>Search Results</h3>
        <div v-for="influencer in searchResults">
            {{ influencer.name }}
            <div>
                <RouterLink :to="`/ad-request/assign?influencer_id=${influencer.id}`">Assign Ad Request</RouterLink> | 
                <RouterLink :to="`/ad-request/create?influencer_id=${influencer.id}`">Create Ad Request</RouterLink>
            </div>
        </div>
    </div>
</template>
