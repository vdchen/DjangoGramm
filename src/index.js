import { createApp } from 'vue';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';

const app = createApp({
    delimiters: ['[[', ']]'],
    data() {
        return {
            isFollowing: false,
            followerCount: 0,
            userId: null,
            csrfToken: null
        }
    },
    mounted() {
        // Look for the element by ID
        const el = document.getElementById('vue-app');

        if (el) {
            // Use getAttribute which is the most basic way to get data
            this.userId = el.getAttribute('data-user-id');
            this.isFollowing = el.getAttribute('data-is-following') === 'true';
            this.followerCount = parseInt(el.getAttribute('data-follower-count')) || 0;

            console.log("MANUAL CHECK - User ID:", this.userId);
        }

        this.csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
    },
    methods: {
        async toggleFollow() {
            // Safety check: if userId is still null, try to grab it one last time
            if (!this.userId) {
                const idTag = document.getElementById('user-id-data');
                if (idTag) this.userId = JSON.parse(idTag.textContent);
            }

            if (!this.userId) {
                console.error("Toggle Follow failed: User ID is still null.");
                return;
            }

            try {
                const response = await fetch(`/users/toggle-follow/${this.userId}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': this.csrfToken,
                        'Content-Type': 'application/json',
                    }
                });


                if (response.ok) {
                    const data = await response.json();
                    this.isFollowing = data.following;
                    this.followerCount = data.count;


                }
            } catch (error) {
                console.error('Follow toggle failed:', error);
            }
        }
    },

});

app.mount('#vue-app');