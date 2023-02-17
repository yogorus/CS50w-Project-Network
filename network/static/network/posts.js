export function load_posts(section, page) {
    var url = `http://127.0.0.1:8000/posts/${section}${page}`;  // Have to be explicit for some reason, otherwise url gets messy
    fetch(url)
    .then(response => response.text())
    .then(posts => {
        // Get template from server
        document.querySelector('#posts-view').innerHTML = posts;
        
        // Add functionality to buttons
        let editBtns = document.querySelectorAll('#edit-btn');
        let saveBtns = document.querySelectorAll('#save-btn');
        let cancelBtns = document.querySelectorAll('#cancel-btn');
        
        editBtns.forEach(e => {
            e.onclick = edit;
        })

        saveBtns.forEach(e => e.style.display = 'none')
        cancelBtns.forEach(e => e.style.display = 'none')

        const prevBtn = document.querySelector('#page-prev');
        const curBtn = document.querySelector('#page-current');
        const nextBtn = document.querySelector('#page-next');
        
        // I don't want '#' appear in the url
        curBtn.addEventListener('click', e => e.preventDefault())
        
        // Add load_posts function to page buttons via recursion
        if (prevBtn) {
            console.log(prevBtn)
            const section = prevBtn.dataset.section;
            const page = `?page=${prevBtn.dataset.page}`;
            prevBtn.addEventListener('click', (e) => {
                e.preventDefault();
                load_posts(section, page);
            });
        }
        if (nextBtn) {
            console.log(nextBtn)
            const section = nextBtn.dataset.section;
            const page = `?page=${nextBtn.dataset.page}`;
            nextBtn.addEventListener('click', (e) => {
                e.preventDefault();
                load_posts(section, page);
            });
        }
    });
}

function edit() {
    // Replace parapraph with text field
    const id = this.dataset.id;
    const post = document.querySelector(`#post-${id}`);
    const csrftoken = post.querySelector('[name=csrfmiddlewaretoken]').value;
    
    const editBtn = this;
    const cancelBtn = post.querySelector('#cancel-btn');
    const saveBtn = post.querySelector('#save-btn');
    
    // Show cancel and save buttons, hide edit
    editBtn.style.display = 'none';
    cancelBtn.style.display = 'block';
    saveBtn.style.display = 'block';

    // Save content of post, get height of parapraph
    let content = post.querySelector('#content');
    let value = content.innerHTML;
    let height = (content.scrollHeight + 10) + "px";    // Adjust textarea 

    // Set up input
    let input = document.createElement('textarea');
    input.style.height = height;
    input.className = 'w-100 mb-1';
    input.value = value;
    content.replaceWith(input);

    // Set autofocus at the end of input field
    const end = input.value.length;
    input.setSelectionRange(end, end);
    input.focus()

    cancelBtn.onclick = () => {
        input.replaceWith(content);
        
        editBtn.style.display = 'block';
        cancelBtn.style.display = 'none';
        saveBtn.style.display = 'none';
    }

    saveBtn.onclick = async () => {
        const url = `http://127.0.0.1:8000/edit/${id}`;
        let response = await fetch(url, {
            method: 'PUT',
            headers: {'X-CSRFToken': csrftoken},
            body: JSON.stringify({
                body: input.value
            })
        });
        response = await response.json();
        console.log(response);
        
        if (response.status) {
            content.innerHTML = input.value.trim();
            input.replaceWith(content);
        
            editBtn.style.display = 'block';
            cancelBtn.style.display = 'none';
            saveBtn.style.display = 'none';
        }
        else {
            input.value = content.innerHTML;
        }
    }
}
