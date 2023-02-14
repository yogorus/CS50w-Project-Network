import {
    load_posts
} from './posts.js';

document.addEventListener('DOMContentLoaded', () => {
    load_posts('all', '?page=')
})