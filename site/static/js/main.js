// View toggle functionality
(function() {
    const viewToggle = document.getElementById('view-toggle');
    const body = document.body;

    // Load saved preference
    const savedView = localStorage.getItem('feedrr-view') || 'list';
    body.classList.add(`view-${savedView}`);

    // Toggle between views
    viewToggle.addEventListener('click', function() {
        if (body.classList.contains('view-cards')) {
            body.classList.remove('view-cards');
            body.classList.add('view-list');
            localStorage.setItem('feedrr-view', 'list');
        } else {
            body.classList.remove('view-list');
            body.classList.add('view-cards');
            localStorage.setItem('feedrr-view', 'cards');
        }
    });
})();
