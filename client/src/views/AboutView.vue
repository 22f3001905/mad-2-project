<script setup>
import Navbar from '@/components/Navbar.vue';

</script>

<template>
    <Navbar />
    <h1>About Us</h1>
    <p>
        Welcome to the Influencer Engagement and Sponsorship Coordination Platform!
    </p>
    <h3>What We Do</h3>
    <p>
        Our platform connects Sponsors and Influencers, fostering impactful collaborations. Sponsors can promote their products or services through influential voices, while influencers monetize their reach by working with renowned brands.
    </p>
    <h3>Key Features</h3>
    <ul>
        <li>
            Effortless Connections: Matchmaking between Sponsors and Influencers based on preferences, audience demographics, and campaign goals.
        </li>
        <li>
            Streamlined Communication: Messaging tools for efficient campaign coordination.
        </li>
        <li>
            Campaign Management: Tools to plan, track, and analyze sponsorship campaigns in real-time.
        </li>
    </ul>
    <h3>Our Technology</h3>
    <p>
        We leverage cutting-edge technology to deliver a seamless experience:
    </p>
    <ul>
        <li>Flask: Backend API framework for flexibility and scalability.</li>
        <li>VueJS: Modern and interactive UI framework for dynamic user interfaces.</li>
        <li>Bootstrap: Sleek and responsive styling for HTML generation.</li>
        <li>SQLite: Lightweight and reliable database for data storage.</li>
        <li>Redis: Efficient caching to boost performance.</li>
        <li>Celery with Redis: Handling batch and scheduled jobs seamlessly.</li>
    </ul>
    <h3>Backend Features</h3>
    <ul>
        <li>
            <strong>Daily Reminders:</strong> Scheduled alerts to influencers via Google Chat Webhooks, SMS, or email, reminding them to check pending ad requests or explore public campaigns.
        </li>
        <li>
            <strong>Monthly Activity Reports:</strong> Automatically generated HTML reports sent via email to sponsors, summarizing campaign activities, growth metrics, and budget utilization.
        </li>
        <li>
            <strong>CSV Export:</strong> Sponsors can trigger an async job from their dashboard to export campaign details as a CSV file, receiving an alert once the job completes.
        </li>
    </ul>
    <p>
        Thank you for choosing our platform. For support, contact us at <a href="mailto:support@sponsorconnect.com">support@sponsorconnect.com</a>.
    </p>
</template>
