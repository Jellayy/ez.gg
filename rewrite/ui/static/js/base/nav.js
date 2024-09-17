document.addEventListener('DOMContentLoaded', () => {
    const pages = document.querySelectorAll('.page');
    const navButtons = document.querySelectorAll('.navButton');
    
    function showPage(pageName) {
        pages.forEach(page => {
            if (page.getAttribute('page') === pageName) {
                page.classList.remove('hidden');
            } else {
                page.classList.add('hidden');
            }
        });
        
        // Update active state in navbar
        navButtons.forEach(button => {
            if (button.getAttribute('page') === pageName) {
                button.classList.add('text-white');
                button.classList.remove('text-[#CBBC8F]');
            } else {
                button.classList.remove('text-white');
                button.classList.add('text-[#CBBC8F]');
            }
        });
    }
    
    navButtons.forEach(button => {
        button.addEventListener('click', () => {
            const pageName = button.getAttribute('page');
            showPage(pageName);
            
            // Update URL without reloading the page
            history.pushState(null, '', `#${pageName}`);
        });
    });

    showPage('index');
    
    // Handle browser back/forward navigation
    window.addEventListener('popstate', () => {
        const currentPage = window.location.hash.slice(1) || 'index';
        showPage(currentPage);
    });
});