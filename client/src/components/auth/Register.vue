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
    reach: null
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
    <h2 class="text-center mb-3 pt-2">Account Registration</h2>
    <div class="row justify-content-center">
        <div class="col-md-6">
            <form @submit.prevent="registerUser" class="p-4 border rounded">
                <h3 class="mb-2 text-center">Basic Info</h3>
                <div class="mb-3">
                    <label for="email" class="form-label">Email</label>
                    <input class="form-control" v-model="form.email" type="text" name="email" id="email" required autocomplete="email" />
                </div>
                <div class="mb-3">
                    <label for="password" class="form-label">Password</label>
                    <input class="form-control" v-model="form.password" type="password" name="password" id="password" required
                        autocomplete="new-password" minlength="6" placeholder="At least 6 characters in length."/>
                </div>
                <div>
                    <label for="accountType" class="form-label">Account Type</label>
                    <select v-model="form.accountType" name="accountType" id="accountType" class="form-select" required>
                        <option value="Sponsor">Sponsor</option>
                        <option value="Influencer">Influencer</option>
                    </select>
                </div>
                <div v-if="form.accountType == 'Sponsor'" class="mt-4">
                    <h3 class="mb-3 text-center">Sponsor Account</h3>
                    <div class="mb-3">
                        <label for="companyName" class="form-label">Company Name</label>
                        <input v-model="sponsor.companyName" class="form-control" type="text" name="companyName"
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
                <div v-else class="mt-4">
                    <h3 class="mb-3 text-center">Influencer Account</h3>
                    <div class="mb-3">
                        <label for="influencerName" class="form-label">Influencer Name</label>
                        <input v-model="influencer.influencerName" class="form-control" type="text"
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
                        <input v-model="influencer.niche" class="form-control" type="text" name="niche"
                            id="niche" required placeholder="Comma separated social media target niches." />
                    </div>
                    <div class="mb-3">
                        <label for="reach" class="form-label">Reach</label>
                        <input v-model="influencer.reach" class="form-control" type="number" name="reach"
                            id="reach" required min="0"
                            placeholder="Total no. of followers on all social media." />
                    </div>
                </div>
                <div class="mt-4">
                    <button type="submit" class="btn btn-primary">Register</button>
                </div>
            </form>
        </div>
    </div>
</template>
