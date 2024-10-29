<script setup>
import { reactive, ref, onMounted } from 'vue';

const searchForm = reactive({
    keyword: null,
});
const searchResults = ref([]);

const searchUsers = async () => {
    try {
        const res = await fetch('/api/search/users', {
            method: 'POST',
            headers: {
                'Authentication-Token': localStorage.getItem('authToken'), 
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                keyword: searchForm.keyword
            })
        });
        const data = await res.json();
        console.log(data);
        searchResults.value = [...data.data];
    } catch (error) {
        console.error('Error in fetching search users results.', error);
    }
}

const resetSearch = () => {
    searchForm.keyword = null;
    searchResults.value = [];
}

const flagUser = async (userId) => {
    try {
        const res = await fetch(`/api/user/${userId}/flag`, {
            method: 'GET',
            headers: { 'Authentication-Token': localStorage.getItem('authToken') }
        });
        const data = await res.json();
        console.log(data);
        searchResults.value.filter(user => user.user_id == userId)[0].flagged = true;
    } catch (error) {
        console.error('Error in flagging user.', error);
    }
}

const unflagUser = async (userId) => {
    try {
        const res = await fetch(`/api/user/${userId}/unflag`, {
            method: 'GET',
            headers: { 'Authentication-Token': localStorage.getItem('authToken') }
        });
        const data = await res.json();
        console.log(data);
        searchResults.value.filter(user => user.user_id == userId)[0].flagged = false;
    } catch (error) {
        console.error('Error in unflagging user.', error);
    }
}
</script>

<template>
    <h2>Search for Users</h2>
    <form @submit.prevent="searchUsers">
        <div class="mb-3">
            <label for="keyword" class="form-label">Search Query</label>
            <input v-model="searchForm.keyword" class="form-control" type="text" name="keyword" id="keyword" aria-describedby="search-keyword">
            <div id="search-keyword" class="form-text">Specify a User search keyword.</div>
        </div>
        <div>
            <button type="submit" class="btn btn-primary">Refine Search</button>
            <button id="reset" type="button" class="btn btn-warning" @click="resetSearch">Reset</button>
        </div>
    </form>
    <div>
        <div v-for="user in searchResults">
            {{ user.name }}
            <div>
                <RouterLink :to="`/user/${user.id}`">View User</RouterLink>
                <button @click="!user.flagged ? flagUser(user.user_id) : unflagUser(user.user_id)">{{ !user.flagged ? 'Flag' : 'Unflag' }}</button>
            </div>
        </div>
    </div>
</template>
