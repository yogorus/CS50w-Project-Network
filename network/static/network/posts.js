export function load_posts(section, page) {
    var url = `http://127.0.0.1:8000/posts/${section}${page}`;  // Have to be explicit for some reason, otherwise url gets messy
    fetch(url)
    .then(response => response.text())
    .then(posts => {
        // Get template from server
        document.querySelector('#posts-view').innerHTML = posts;
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
