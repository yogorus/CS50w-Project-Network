import { load_posts } from "./posts.js";

document.addEventListener('DOMContentLoaded', () => {

const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

if (document.querySelector('#new-post')) {
    document.querySelector('#id_body').value = '';
    
    document.querySelector('#new-post').onsubmit = (e) => {
        e.preventDefault();
        fetch('/new_post', {
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            body: JSON.stringify({
                body: `${document.querySelector('#id_body').value}`
            })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result),
            document.querySelector('#id_body').value = '';
            load_posts(section, '')
        })
    
        return false;
    }
}

})

