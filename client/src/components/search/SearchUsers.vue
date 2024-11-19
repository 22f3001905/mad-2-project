<script setup>
import { reactive, ref, onMounted } from 'vue';
import { formatNumber } from '@/utils';

const searchForm = reactive({
    keyword: null,
    userType: 'Sponsor',
});
const searchResults = ref([]);
const searched = ref(false);

const searchUsers = async () => {
    try {
        const res = await fetch('/api/search/users', {
            method: 'POST',
            headers: {
                'Authentication-Token': localStorage.getItem('authToken'), 
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                keyword: searchForm.keyword,
                user_type: searchForm.userType
            })
        });
        const data = await res.json();
        console.log(data);
        searchResults.value = [...data.data];
        searched.value = true;
    } catch (error) {
        console.error('Error in fetching search users results.', error);
    }
}

const resetSearch = () => {
    searchForm.keyword = null;
    searchForm.userType = 'Sponsor';
    searchResults.value = [];
    searched.value = false;
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
    <h2 class="text-center mb-3 pt-2">Search for Users</h2>

    <div class="row my-4 justify-content-center">
        <div class="col-md-6">
            <form @submit.prevent="searchUsers" class="p-4 border rounded shadow-sm">
                <div class="mb-3">
                    <label for="keyword" class="form-label">Search Query</label>
                    <input v-model="searchForm.keyword" class="form-control" type="text" name="keyword" id="keyword" aria-describedby="search-keyword">
                    <div id="search-keyword" class="form-text">Specify a User search keyword.</div>
                </div>

                <div class="mb-3">
                    <label for="user-type" class="form-label">User Type</label>
                    <select v-model="searchForm.userType" name="user-type" id="user-type" class="form-select" required>
                         <option value="Sponsor">Sponsor</option>
                         <option value="Influencer">Influencer</option>
                    </select>
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
            v-for="user in searchResults" 
            :key="user.id" 
            class="col-md-4 mb-4"
        >
            <div class="card shadow-sm h-100">
                <div class="card-body d-flex flex-column">
                    <h3 class="card-title">{{ user.name }}</h3>

                    <ul class="list-unstyled">
                        <li>
                            <strong>Type:</strong> {{ user.role }}
                        </li>
                        <li>
                            <strong>Email:</strong> {{ user.email }}
                        </li>
                        <li>
                            <strong>Wallet:</strong> Rs. {{ formatNumber(user.wallet) }}
                        </li>
                    </ul>

                    <div class="d-flex gap-2 mt-auto">
                        <RouterLink 
                            :to="`/user/${user.user_id}`" 
                            class="btn btn-primary btn-sm"
                        >
                            View User
                        </RouterLink>
                        <button 
                            @click="!user.flagged ? flagUser(user.user_id) : unflagUser(user.user_id)" 
                            class="btn btn-warning btn-sm"
                        >
                            {{ !user.flagged ? 'Flag' : 'Unflag' }}
                        </button>
                    </div>
                </div>
            </div>
        </div>
        <p v-if="searchResults.length == 0 && searched" class="text-center">
            No users found.
        </p>
    </div>
</template>
