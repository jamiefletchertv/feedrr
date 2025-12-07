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

// Filter functionality
(function() {
    const categoryFilter = document.getElementById('category-filter');
    const topicFilter = document.getElementById('topic-filter');
    const filterStatus = document.querySelector('.filter-status');
    const articles = document.querySelectorAll('.article');

    function applyFilters() {
        const selectedCategory = categoryFilter.value;
        const selectedTopic = topicFilter.value;

        let visibleCount = 0;

        articles.forEach(article => {
            const articleCategory = article.dataset.category || 'none';
            const articleTopics = article.dataset.topics ? article.dataset.topics.split(',') : [];

            // Check category filter
            const categoryMatch = selectedCategory === 'all' || articleCategory === selectedCategory;

            // Check topic filter
            const topicMatch = selectedTopic === 'all' || articleTopics.includes(selectedTopic);

            // Show article only if it matches both filters
            if (categoryMatch && topicMatch) {
                article.style.display = '';
                visibleCount++;
            } else {
                article.style.display = 'none';
            }
        });

        // Update status message
        updateFilterStatus(selectedCategory, selectedTopic, visibleCount);
    }

    function updateFilterStatus(category, topic, count) {
        if (category === 'all' && topic === 'all') {
            filterStatus.textContent = '';
            filterStatus.classList.remove('active');
        } else {
            const parts = [];
            if (category !== 'all') {
                parts.push(category.charAt(0).toUpperCase() + category.slice(1));
            }
            if (topic !== 'all') {
                parts.push(topic);
            }
            filterStatus.textContent = `Showing ${count} ${parts.join(' • ')} article${count !== 1 ? 's' : ''}`;
            filterStatus.classList.add('active');
        }
    }

    // Handle filter changes
    categoryFilter.addEventListener('change', applyFilters);
    topicFilter.addEventListener('change', applyFilters);
})();

// Expandable article content
(function() {
    // Only handle expandable articles
    const expandableHeaders = document.querySelectorAll('.article-header.expandable');

    expandableHeaders.forEach(header => {
        header.addEventListener('click', function(e) {
            const article = this.closest('.article');

            // Toggle expanded state
            article.classList.toggle('expanded');
        });
    });

    // Prevent link button clicks from triggering article expansion
    const linkButtons = document.querySelectorAll('.article-link-btn');
    linkButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    });
})();
