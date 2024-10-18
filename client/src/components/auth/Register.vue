<script setup>
import { reactive, ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const industries = ref([]);
const influencerCategories = ref([]);

onMounted(async () => {
    try {
        const response = await fetch('/api/hard-coded-form-data');
        const data = await response.json();
        const fetchedIndustries = [];
        for (const [idx, industryName] of data.industry_names.entries()) {
            fetchedIndustries.push({ id: idx + 1, name: industryName });
        }
        industries.value = [...fetchedIndustries];
        const fetchedInfluencerCategories = [];
        for (const [idx, categoryName] of data.influencer_category_names.entries()) {
            fetchedInfluencerCategories.push({ id: idx + 1, name: categoryName });
        }
        influencerCategories.value = [...fetchedInfluencerCategories];
    } catch (error) {
        console.error('Error fetching hard coded form data.', error);
    }
});

const form = reactive({
    email: '',
    password: '',
    accountType: 'Sponsor'
});
const sponsor = reactive({
    companyName: '',
    industryId: 1
});
const influencer = reactive({
    influencerName: '',
    categoryId: 1,
    niche: '',
    reach: 0
});

const registerUser = async () => {
    const userData = { email: form.email, password: form.password, roles: [form.accountType] };
    let requestBody = {}
    if (form.accountType == 'Sponsor') {
        requestBody = {
            ...userData, 
            companyName: sponsor.companyName, 
            industryId: sponsor.industryId
        };
    } else {
        requestBody = {
            ...userData, 
            influencerName: influencer.influencerName, 
            categoryId: influencer.categoryId, 
            niche: influencer.niche, 
            reach: influencer.reach
        };
    }
    try {
        const response = await fetch('/api/user/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(requestBody)
        });
        const data = await response.json();
        console.log(data);
        router.push('/login');
    } catch (error) {
        console.error('Error creating user account.', error);
    }
};
</script>

<template>
    <form @submit.prevent="registerUser">
        <h2>Basic Info</h2>
        <div class="mb-3">
            <label for="email" class="form-label">Email</label>
            <input v-model="form.email" type="text" name="email" id="email" required autocomplete="email" />
        </div>
        <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <input v-model="form.password" type="password" name="password" id="password" required
                autocomplete="new-password" minlength="6" />
        </div>
        <div>
            <label for="accountType">Account Type</label>
            <select v-model="form.accountType" name="accountType" id="accountType" required>
                <option value="Sponsor">Sponsor</option>
                <option value="Influencer">Influencer</option>
            </select>
        </div>
        <div v-if="form.accountType == 'Sponsor'">
            <h2>Sponsor Account</h2>
            <div class="mb-3">
                <label for="companyName" class="form-label">Company Name</label>
                <input v-model="sponsor.companyName" class="form-control form-control-sm" type="text" name="companyName"
                    id="companyName" required />
            </div>
            <div class="mb-3">
                <label for="industryId" class="form-label">Industry</label>
                <select v-model="sponsor.industryId" name="industryId" id="industryId" class="form-select" required>
                    <option v-for="industry in industries" :value="industry.id" :key="industry.id">
                        {{ industry.name }}
                    </option>
                </select>
            </div>
        </div>
        <div v-else>
            <h2>Influencer Account</h2>
            <div class="mb-3">
                <label for="influencerName" class="form-label">Influencer Name</label>
                <input v-model="influencer.influencerName" class="form-control form-control-sm" type="text"
                    name="influencerName" id="influencerName" required />
            </div>
            <div class="mb-3">
                <label for="categoryId" class="form-label">Category</label>
                <select v-model="influencer.categoryId" name="categoryId" id="categoryId" class="form-select" required>
                    <option v-for="category in influencerCategories" :value="category.id" :key="category.id">
                        {{ category.name }}
                    </option>
                </select>
            </div>
            <div class="mb-3">
                <label for="niche" class="form-label">Niches</label>
                <input v-model="influencer.niche" class="form-control form-control-sm" type="text" name="niche"
                    id="niche" required placeholder="Comma separated social media target niches." />
            </div>
            <div class="mb-3">
                <label for="reach" class="form-label">Reach</label>
                <input v-model="influencer.reach" class="form-control form-control-sm" type="number" name="reach"
                    id="reach" required min="0"
                    placeholder="Total number of followers on all social media. (Nearest 1,000)." />
            </div>
        </div>
        <div>
            <button type="submit">Register</button>
        </div>
    </form>
</template>
