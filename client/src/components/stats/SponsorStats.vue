<script setup>
import Chart from '@/components/stats/Chart.vue';
import { onMounted, reactive } from 'vue';

const zip = (a, b) => a.map((k, i) => [k, b[i]]);

const campaignNames = [];

const chartData = reactive({
    adRequestStatusData: {},
    adRequestPayoutData: [],
    adRequestPayoutAggData: {},
    campaignsBudgetData: {}
});

const barChartOptions = {
    indexAxis: 'y',
}

onMounted(async () => {
    try {
        const res = await fetch('/api/sponsor/stats', {
            headers: {
                'Authentication-Token': localStorage.getItem('authToken')
            }
        });
        const data = await res.json();
        console.log(data);

        chartData.adRequestStatusData = {
            labels: Object.keys(data.ad_request_status),
            datasets: [
                {
                    label: 'Ad Request Status',
                    data: Object.values(data.ad_request_status),
                    hoverOffset: 4,
                }
            ]
        }

        for (const payout of data.ad_request_payout) {
            const { campaign_name } = payout;
            campaignNames.push(campaign_name);
            delete payout.campaign_name;

            chartData.adRequestPayoutData.push({ 
                labels: Object.keys(payout),
                datasets: [
                    {
                        label: 'Ad Request Payout',
                        data: Object.values(payout),
                        hoverOffset: 4,
                    }
                ]
            })
        }

        chartData.adRequestPayoutAggData = {
            labels: Object.keys(data.ad_request_payout_agg),
            datasets: [
                {
                    label: 'Ad Request Payout',
                    data: Object.values(data.ad_request_payout_agg),
                    hoverOffset: 4,
                }
            ]
        }

        chartData.campaignsBudgetData = {
            labels: data.campaigns.map(camp => camp.name),
            datasets: [
                {
                    label: 'Ad Request Status',
                    data: data.campaigns.map(camp => camp.budget),
                    hoverOffset: 4,
                }
            ]
        }
    } catch (error) {
        console.error('Error fetching charts data.', error);
    }
});
</script>

<template>
    <div>
        <h1>Sponsor Statistics</h1>
        <div class="row" v-if="chartData.adRequestStatusData.labels">
            <h2>Ad Request Status</h2>
            <Chart :chartData="chartData.adRequestStatusData" chartType="doughnut" style="width: 325px;" />
            <table class="table table-bordered border-secondary align-middle text-center col">
                <thead>
                    <tr>
                        <th>Ad Request Status</th>
                        <th>No. of Ad Requests</th>
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
        <div class="row mt-5" v-if="chartData.adRequestPayoutData.length">
            <h2>Ad Request Payout</h2>
            <div class="col-md-6 d-flex justify-content-center mt-3" v-for="[campaignName, adPayoutData] in zip(campaignNames, chartData.adRequestPayoutData)">
                <div class="text-center">
                    <h3 class="mt-3">{{ campaignName }}</h3>
                    <Chart :chartData="adPayoutData" chartType="bar" style="width: 375px;" :chartOptions="barChartOptions" />
                </div>
            </div>
        </div>
        <div class="row mt-5" v-if="chartData.adRequestPayoutAggData.labels">
            <h2>Ad Request Payout (Aggregated)</h2>
            <table class="table table-bordered border-secondary align-middle text-center col">
                <thead>
                    <tr>
                        <th>Ad Request Status</th>
                        <th>Total Payout</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="[status, val] in zip(chartData.adRequestPayoutAggData.labels, chartData.adRequestPayoutAggData.datasets[0].data)">
                        <td>{{ status }}</td>
                        <td>{{ val }}</td>
                    </tr>
                    <tr>
                        <th>Total</th>
                        <th>{{ chartData.adRequestPayoutAggData.datasets[0].data.reduce((a, b) => a + b, 0) }}</th>
                    </tr>
                </tbody>
            </table>
            <Chart :chartData="chartData.adRequestPayoutAggData" chartType="pie" style="width: 325px;" />
        </div>
        <div class="row mt-5" v-if="chartData.campaignsBudgetData.labels">
            <h2>Remaining Campaign Budget Allocation</h2>
            <Chart :chartData="chartData.campaignsBudgetData" chartType="polarArea" style="width: 400px;" />
            <table class="table table-bordered border-secondary align-middle text-center col">
                <thead>
                    <tr>
                        <th>Campaign Name</th>
                        <th>Budget</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="[campaign_name, val] in zip(chartData.campaignsBudgetData.labels, chartData.campaignsBudgetData.datasets[0].data)">
                        <td>{{ campaign_name }}</td>
                        <td>{{ val }}</td>
                    </tr>
                    <tr>
                        <th>Total</th>
                        <th>{{ chartData.campaignsBudgetData.datasets[0].data.reduce((a, b) => a + b, 0) }}</th>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>
