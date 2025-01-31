<script setup>
import { onMounted, ref, reactive, onUnmounted, onBeforeUnmount } from 'vue';
import { redirectToErrorPage } from '@/utils';
import { useRouter } from 'vue-router';

const router = useRouter();

const showDownloadButton = ref(true);
const exportCompleted = ref(false);
const downloadButtonManual = ref(null);

const message = ref('Waiting for download...');

const state = reactive({
    polls: [],
    taskResult: null,
});

let intervalId = null; // Declare the intervalId outside to manage it properly

const downloadCampaignsCSVFile = async (url) => {
    try {
        const res = await fetch(url, {
            method: 'GET',
            headers: { 'Authentication-Token': localStorage.getItem('authToken') }
        });

        if (res.ok) {
            exportCompleted.value = true;
            const blob = await res.blob();
            const url = window.URL.createObjectURL(blob);
            
            downloadButtonManual.value.href = url;
            downloadButtonManual.value.download = "campaigns.csv";
            downloadButtonManual.value.click();

            setTimeout(() => {
                window.URL.revokeObjectURL(url);
            }, 10000);
        } else {
            console.error('Error in download request.', res.statusText);
            return redirectToErrorPage(res.status, router);
        }
    } catch (error) {
        console.error('Error in downloading .csv file.', error);
    }
}

const triggerExport = async () => {
    try {
        console.log('Triggered Export');
        showDownloadButton.value = false;
        message.value = 'Export in progress...';

        const res = await fetch('/api/campaigns/download', {
            method: 'GET',
            headers: { 'Authentication-Token': localStorage.getItem('authToken') }
        });

        if (!res.ok) {
            return redirectToErrorPage(res.status, router);
        }

        const data = await res.json();
        console.log(data);

        localStorage.setItem('taskId', data.task_id);

        let pollCounter = 0;

        intervalId = setInterval(async () => {
            await poll(data.task_id);
            pollCounter++;
            if (pollCounter >= 10){
                clearInterval(intervalId);
                message.value = 'Something went wrong! Please try again later.';
                localStorage.removeItem('taskId');
            }
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

        if (!res.ok) {
            localStorage.removeItem('taskId');
            return redirectToErrorPage(res.status, router);
        }

        const data = await res.json();
        console.log(data);

        if (data.ready) {
            state.taskResult = data.value;
            message.value = 'Download is ready!';

            const pollId = state.polls.shift();
            clearInterval(pollId);
            localStorage.removeItem('taskId');

            console.log('DATA IS READY TO BE DOWNLOADED.', data.value);
            await downloadCampaignsCSVFile(data.value.download_link);

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
        let pollCounter = 0;

        intervalId = setInterval(async () => {
            await poll(taskId);
            pollCounter++;
            if (pollCounter >= 10){
                clearInterval(intervalId);
                message.value = 'Something went wrong! Please try again later.';
                localStorage.removeItem('taskId');
            }
        }, 5000);

        state.polls.push(intervalId);
    } else {
        console.log('No tasks triggered!');
    }
});

// Important: We need to clear the polling before unmounting this component.
onBeforeUnmount(() => {
    const pollId = state.polls.shift();
    clearInterval(pollId);
})
</script>

<template>
    <div class="p-3 border rounded shadow-sm alert alert-primary">
        <div class="d-flex align-items-center justify-content-start">
            <p class="mb-0">
                <strong>
                    Export campaign data as a .csv file:
                </strong>
            </p>
            <button 
                @click="triggerExport" 
                v-if="showDownloadButton" 
                class="btn btn-light ms-2"
            >
                Download
            </button>
            <div v-else>
                <p class="mb-0 ms-2"> {{ message }}</p>
            </div>
        </div>
        <p v-if="exportCompleted" class="mb-0 mt-3">
            Didn't download automatically? 
            <a ref="downloadButtonManual" class="link">
                Click Here
            </a>
        </p>
    </div>
</template>
