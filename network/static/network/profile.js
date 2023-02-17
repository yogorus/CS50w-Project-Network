import {
    load_posts
} from './posts.js';

document.addEventListener('DOMContentLoaded', () => {
    load_posts(section, '');
    let followBtn = document.querySelector('#follow-btn');
    if (followBtn) {
        if (userIsFollower) {
            followBtn.innerHTML = 'Unfollow';
            followBtn.onclick = unfollow;
        }
        else {
            followBtn.innerHTML = 'Follow';
            followBtn.onclick = follow;
        }
    }
})

const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const url = `http://127.0.0.1:8000/profile/${section}/follow`;
let followers = parseInt(document.querySelector('#followers').innerHTML);

function follow() {
    fetch(url, {
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken}
    })
    .then(response => response.json())
    .then(message => {
        console.log(message);
        this.innerHTML = 'Unfollow';
        this.onclick = unfollow;
        followers++;
        document.querySelector('#followers').innerHTML = followers;
    })
}

function unfollow() {
    fetch(url, {
        method: 'DELETE',
        headers: {'X-CSRFToken': csrftoken}
    })
    .then(response => response.json())
    .then(message => {
        console.log(message);
        this.innerHTML = 'Follow';
        this.onclick = follow;
        followers--;
        document.querySelector('#followers').innerHTML = followers;
    })
}