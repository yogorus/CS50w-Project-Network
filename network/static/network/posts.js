export function load_posts(section, page) {
    var url = `http://127.0.0.1:8000/posts/${section}${page}`;
    fetch(url)
    .then(response => response.text())
    .then(posts => {
        // console.log(posts);
        document.querySelector('#posts-view').innerHTML = posts;
        const prevBtn = document.querySelector('#page-prev');
        const curBtn = document.querySelector('#page-current');
        const nextBtn = document.querySelector('#page-next');
        
        curBtn.addEventListener('click', e => e.preventDefault())
        
        // Add load posts function to page btns
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
    })
}
