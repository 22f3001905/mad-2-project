<script setup>
import Chart from '@/components/stats/Chart.vue';
import { onMounted, reactive } from 'vue';

const zip = (a, b) => a.map((k, i) => [k, b[i]]);

const chartData = reactive({
    adRevenueData: {},
    adRequestSentData: {},
    adRequestStatusData: {},
});

onMounted(async () => {
    try {
        const res = await fetch('/api/influencer/stats', {
            headers: {
                'Authentication-Token': localStorage.getItem('authToken')
            }
        });
        const data = await res.json();
        console.log(data);

        const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

        chartData.adRevenueData = {
            labels: months.filter((val, idx) => data.monthly_ad_revenue[idx] > 0),
            datasets: [
                {
                    label: 'Ad Request Monthly Revenue',
                    backgroundColor: '#42A5F5',
                    data: data.monthly_ad_revenue.filter(revenue => revenue > 0)
                },
            ],
        };

        chartData.adRequestSentData = {
            labels: ['Sent', 'Received'],
            datasets: [
                {
                    label: 'Ad Request Initialization', 
                    data: [data.ad_request_initialize.sent, data.ad_request_initialize.received], 
                    // backgroundColor: ['rgb(123, 104, 238)', 'rgb(50, 205, 50)'], 
                    hoverOffset: 4,
                }
            ]
        }

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
    } catch (error) {
        console.error('Error fetching charts data.', error);
    }
});
</script>

<template>
    <div>
        <h1>Influencer Statistics</h1>
        <div class="row mt-2">
            <div>
                <h2>Monthly Ad Revenue <span>*Potential</span></h2>
            </div>
            <Chart v-if="chartData.adRevenueData.labels" :chartData="chartData.adRevenueData" chartType="bar" />
        </div>
        <div class="row mt-5">
            <h2>Ad Requests Sent</h2>
            <div class="row" v-if="chartData.adRequestSentData.datasets">
                <table class="table table-bordered border-secondary align-middle text-center col">
                    <thead>
                        <tr>
                            <th>Sender</th>
                            <th>No. of Requests</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>You</td>
                            <td>{{ chartData.adRequestSentData.datasets[0].data[0] }}</td>
                        </tr>
                        <tr>
                            <td>Sponsor</td>
                            <td>{{ chartData.adRequestSentData.datasets[0].data[1] }}</td>
                        </tr>
                        <tr>
                            <th>Total</th>
                            <th>
                                {{ chartData.adRequestSentData.datasets[0].data.reduce((a, b) => a + b, 0) }}
                            </th>
                        </tr>
                    </tbody>
                </table>
                <Chart :chartData="chartData.adRequestSentData" chartType="doughnut" style="width: 300px;" />
            </div>
        </div>
        <div class="row mt-5" v-if="chartData.adRequestStatusData.labels">
            <h2>Ad Request Status</h2>
            <Chart :chartData="chartData.adRequestStatusData" chartType="pie" style="width: 325px;" />
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
    </div>
</template>
