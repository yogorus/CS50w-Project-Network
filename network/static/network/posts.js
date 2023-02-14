export function load_posts(section, page) {
    fetch(`posts/${section}${page}`)
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
    // .then(() => {
    //     const prevBtn = document.querySelector('#page-prev');
    //     const nextBtn = document.querySelector('#page-next');
    //     // console.log(prevBtn)
    //     // console.log(nextBtn)
        
    //     // Add load posts function to page btns
    //     if (!prevBtn === null) {
    //         console.log(prevBtn)
    //         const section = prevBtn.dataset.section;
    //         const page = prevBtn.value
    //         prevBtn.addEventListener('click', () => load_posts(section, page));
    //     }
    //     if (!nextBtn === null) {
    //         console.log(nextBtn)
    //         const section = nextBtn.dataset.section;
    //         const page = nextBtn.dataset.page;
    //         console.log(page)
    //         nextBtn.addEventListener('click', () => load_posts(section, page));
    //     }
    // });
}
