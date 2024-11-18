<script setup>
import Chart from '@/components/stats/Chart.vue';
import { onMounted, reactive } from 'vue';
import { formatNumber } from '@/utils';

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
        <section 
            class="row mt-4" 
            v-if="chartData.adRequestStatusData.labels"
        >
            <div class="col-12 text-center">
                <h2 class="mb-4">Ad Request Status</h2>
            </div>

            <div 
                class="col-md-6 d-flex justify-content-center align-items-center"
            >
                <Chart 
                    :chartData="chartData.adRequestStatusData" 
                    chartType="doughnut" 
                    style="width: 350px;" 
                />
            </div>

            <div 
                class="col-md-6 d-flex justify-content-center align-items-center"
            >
                <table 
                    class="table table-striped table-hover table-bordered border-secondary align-middle text-center"
                >
                    <thead class="table-dark">
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
        </section>

        <section 
            class="row mt-5" 
            v-if="chartData.adRequestPayoutData.length"
        >
            <div class="col-12 text-center">
                <h2 class="mb-4">Ad Request Payout</h2>
            </div>

            <div 
                class="col-md-6 d-flex justify-content-center align-items-center" 
                v-for="[campaignName, adPayoutData] in zip(campaignNames, chartData.adRequestPayoutData)"
            >
                <div class="text-center mb-4">
                    <h3 class="mt-3">{{ campaignName }}</h3>
                    <Chart 
                        :chartData="adPayoutData" 
                        chartType="bar" 
                        style="width: 350px;" 
                        :chartOptions="barChartOptions" 
                    />
                </div>
            </div>
        </section>

        <section 
            class="row mt-5" 
            v-if="chartData.adRequestPayoutAggData.labels"
        >
            <div class="col-12 text-center">
                <h2 class="mb-4">Ad Request Payout (Status)</h2>
            </div>

            <div 
                class="col-md-6 d-flex justify-content-center align-items-center"
            >
                <table class="table table-striped table-hover table-bordered border-secondary align-middle">
                    <thead class="table-dark text-center">
                        <tr>
                            <th>Ad Request Status</th>
                            <th>Total Payout</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="[status, val] in zip(chartData.adRequestPayoutAggData.labels, chartData.adRequestPayoutAggData.datasets[0].data)">
                            <td>{{ status }}</td>
                            <td class="d-flex justify-content-between align-items-center">
                                <span>Rs.</span>
                                <span>{{ formatNumber(val) }}</span>
                            </td>
                        </tr>
                        <tr>
                            <th>Total</th>
                            <th class="d-flex justify-content-between align-items-center">
                                <span>Rs.</span>
                                <span>
                                    {{ formatNumber(chartData.adRequestPayoutAggData.datasets[0].data.reduce((a, b) => a + b, 0)) }}
                                </span>
                            </th>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div 
                class="col-md-6 d-flex justify-content-center align-items-center"
            >
                <Chart 
                    :chartData="chartData.adRequestPayoutAggData" 
                    chartType="doughnut" 
                    style="width: 350px;" 
                />
            </div>
        </section>

        <section 
            class="row mt-5" 
            v-if="chartData.campaignsBudgetData.labels"
        >
            <div class="col-12 text-center">
                <h2 class="mb-4">Campaign Budget Allocation</h2>
            </div>

            <div 
                class="col-md-6 d-flex justify-content-center align-items-center"
            >
                <Chart 
                    :chartData="chartData.campaignsBudgetData" 
                    chartType="polarArea" 
                    style="width: 350px;" 
                />
            </div>

            <div 
                class="col-md-6 d-flex justify-content-center align-items-center"
            >
                <table class="table table-striped table-hover table-bordered border-secondary align-middle">
                    <thead class="table-dark text-center">
                        <tr>
                            <th>Campaign Name</th>
                            <th>Budget</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="[campaign_name, val] in zip(chartData.campaignsBudgetData.labels, chartData.campaignsBudgetData.datasets[0].data)">
                            <td>{{ campaign_name }}</td>
                            <td class="d-flex justify-content-between align-items-center">
                                <span>Rs.</span>
                                <span>{{ formatNumber(val) }}</span>
                            </td>
                        </tr>
                        <tr>
                            <th>Total</th>
                            <th class="d-flex justify-content-between align-items-center">
                                <span>Rs.</span>
                                <span>
                                    {{ formatNumber(chartData.campaignsBudgetData.datasets[0].data.reduce((a, b) => a + b, 0)) }}
                                </span>
                            </th>
                        </tr>
                    </tbody>
                </table>
            </div>
        </section>
    </div>
</template>
