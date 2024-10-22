<script setup>
import { onMounted, ref, reactive } from 'vue';

const showDownloadButton = ref(true);
const message = ref('Waiting for download...');

const state = reactive({
    polls: [],
    taskResult: null,
});

let intervalId = null; // Declare the intervalId outside to manage it properly

const triggerExport = async () => {
    try {
        console.log('Triggered Export');
        showDownloadButton.value = false;
        message.value = 'Export in progress...';

        const res = await fetch('/api/campaigns/download', {
            method: 'GET',
            headers: { 'Authentication-Token': localStorage.getItem('authToken') }
        });
        const data = await res.json();
        console.log(data);

        localStorage.setItem('taskId', data.task_id);

        intervalId = setInterval(() => {
            poll(data.task_id);
        }, 5000);

        state.polls.push(intervalId);
    } catch (error) {
        console.error('Error in triggering campaign data export.', error);
        message.value = 'Error triggering export.';
    }
};

const poll = async (taskId) => {
    try {
        const res = await fetch(`/api/exports/${taskId}`, {
            method: 'GET',
            headers: { 'Authentication-Token': localStorage.getItem('authToken') }
        });
        const data = await res.json();

        if (data.ready) {
            state.taskResult = data.value;
            message.value = 'Download is ready!';

            const pollId = state.polls.shift();
            clearInterval(pollId);
            localStorage.removeItem('taskId');

            // TODO: Trigger .csv file download.
            console.log('DATA IS READY TO BE DOWNLOADED.');

        } else {
            message.value = 'Still processing export...';
        }
    } catch (error) {
        console.error(`Error in polling for task: ${taskId}`, error);
        message.value = 'Error polling export status.';
    }
};

onMounted(() => {
    const taskId = localStorage.getItem('taskId');
    if (taskId) {
        showDownloadButton.value = false;
        message.value = 'Resuming export process...';

        intervalId = setInterval(() => {
            poll(taskId);
        }, 5000);

        state.polls.push(intervalId);
    } else {
        console.log('No tasks triggered!');
    }
});
</script>

<template>
    <div>
        <p>Export campaign data as a .csv file: </p>
        <button @click="triggerExport" v-if="showDownloadButton">Download</button>
        <p v-else>{{ message }}</p>
    </div>
</template>
