<script setup>
import Chart from '@/components/stats/Chart.vue';
import { onMounted, reactive } from 'vue';

const zip = (a, b) => a.map((k, i) => [k, b[i]]);
const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

const chartData = reactive({
    activeUsersData: {},
    campaignInfoData: {},
    monthlyCampaignsData: {},
    adRequestStatusData: {},
    monthlyAdRequestPaymentsData: {}
});

onMounted(async () => {
    try {
        const res = await fetch('/api/admin/stats', {
            headers: {
                'Authentication-Token': localStorage.getItem('authToken')
            }
        });
        const data = await res.json();
        console.log(data);

        chartData.activeUsersData = {
            labels: Object.keys(data.active_users),
            datasets: [
                {
                    label: 'Active Users',
                    data: Object.values(data.active_users),
                    hoverOffset: 4,
                }
            ]
        }
        chartData.campaignInfoData = {
            labels: Object.keys(data.campaigns_info),
            datasets: [
                {
                    label: 'Active Users',
                    data: Object.values(data.campaigns_info),
                    hoverOffset: 4,
                }
            ]
        }
        chartData.monthlyCampaignsData = {
            labels: months.filter((_, i) => data.monthly_campaigns[i] > 0),
            datasets: [
                {
                    label: 'Monthly Campaigns',
                    data: data.monthly_campaigns.filter(count => count > 0),
                    hoverOffset: 4,
                }
            ]
        }
        chartData.adRequestStatusData = {
            labels: Object.keys(data.ad_request_statuses),
            datasets: [
                {
                    label: 'Ad Request Status',
                    data: Object.values(data.ad_request_statuses),
                    hoverOffset: 4,
                }
            ]
        }
        chartData.monthlyAdRequestPaymentsData = {
            labels: months.filter((_, i) => data.monthly_ad_request_payments[i] > 0),
            datasets: [
                {
                    label: 'Monthly Revenue',
                    data: data.monthly_ad_request_payments.filter(count => count > 0),
                    hoverOffset: 4,
                }
            ]
        }
        // console.log(chartData);
    } catch (error) {
        console.error('Error fetching charts data.', error);
    }
});
</script>

<template>
    <div>
        <h1>Admin Statistics</h1>
        <div class="row mt-2" v-if="chartData.activeUsersData.labels">
            <h2>Active Users</h2>
            <Chart :chartData="chartData.activeUsersData" chartType="doughnut" style="width: 325px;" />
            <table class="table table-bordered border-secondary align-middle text-center col">
                <thead>
                    <tr>
                        <th>User Type</th>
                        <th>No. of Users</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="[userType, val] in zip(chartData.activeUsersData.labels, chartData.activeUsersData.datasets[0].data)">
                        <td>{{ userType }}</td>
                        <td>{{ val }}</td>
                    </tr>
                    <tr>
                        <th>Total</th>
                        <th>{{ chartData.activeUsersData.datasets[0].data.reduce((a, b) => a + b, 0) }}</th>
                    </tr>
                </tbody>
            </table>
        </div>
        <div class="row mt-5" v-if="chartData.campaignInfoData.labels">
            <h2>Campaign Info</h2>
            <table class="table table-bordered border-secondary align-middle text-center col">
                <thead>
                    <tr>
                        <th>Campaign Type</th>
                        <th>No. of Campaigns</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="[campaignType, val] in zip(chartData.campaignInfoData.labels, chartData.campaignInfoData.datasets[0].data)">
                        <td>{{ campaignType }}</td>
                        <td>{{ val }}</td>
                    </tr>
                    <tr>
                        <th>Total</th>
                        <th>{{ chartData.campaignInfoData.datasets[0].data.reduce((a, b) => a + b, 0) }}</th>
                    </tr>
                </tbody>
            </table>
            <Chart :chartData="chartData.campaignInfoData" chartType="pie" style="width: 325px;" />
        </div>
        <div class="row mt-5" v-if="chartData.monthlyCampaignsData.labels">
            <h2>Monthly Campaigns</h2>
            <Chart :chartData="chartData.monthlyCampaignsData" chartType="bar" class="mb-3" />
            <p>Note: Filtered out those months where no campaigns were created.</p>
        </div>
        <div class="row mt-5" v-if="chartData.adRequestStatusData.labels">
            <h2>Ad Request Status</h2>
            <Chart :chartData="chartData.adRequestStatusData" chartType="doughnut" style="width: 325px;" />
            <table class="table table-bordered border-secondary align-middle text-center col">
                <thead>
                    <tr>
                        <th>Ad Request Status</th>
                        <th>No. of Ads</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="[status, val] in zip(chartData.adRequestStatusData.labels, chartData.adRequestStatusData.datasets[0].data)">
                        <td>{{ status }}</td>
                        <td>{{ val }}</td>
                    </tr>
                    <tr>
                        <th>Total</th>
                        <th>{{ chartData.adRequestStatusData.datasets[0].data.reduce((a, b) => a + b, 0) }}</th>
                    </tr>
                </tbody>
            </table>
        </div>
        <div class="row mt-5" v-if="chartData.monthlyAdRequestPaymentsData.labels">
            <h2>Monthly Ad Request Revenue</h2>
            <p>Revenue: 5% commission fee on payment of a "Completed" Ad Request.</p>
            <Chart :chartData="chartData.monthlyAdRequestPaymentsData" chartType="bar" class="mb-3" />
        </div>
    </div>
</template>
