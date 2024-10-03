<script setup>
import { onMounted, reactive, ref } from 'vue';

const searchForm = reactive({
    'min_reach': null,
    'category_id': '',
    'niche': null,
});

const influencerCategories = ref([]);

const searchInfluencers = async () => {
    console.log('Search influencers.');
    try {
        const res = await fetch('/api/search/influencers', {
            method: 'POST',
            headers: {
                'Authentication-Token': sessionStorage.getItem('authToken'), 
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
    } catch (error) {
        console.error('Error in fetching search influencers results.', error);
    }
}

const resetSearch = () => {
    searchForm.min_reach = null
    searchForm.category_id = ''
    searchForm.niche = null
    searchInfluencers();
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
    <form @submit.prevent="searchInfluencers">
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
            <!-- <button id="reset" type="button" class="btn btn-warning" onclick="window.location.reload()">Reset</button> -->
            <button id="reset" type="button" class="btn btn-warning" @click="resetSearch">Reset</button>
        </div>
    </form>
</template>
