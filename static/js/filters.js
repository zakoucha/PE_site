document.addEventListener('DOMContentLoaded', function() {
  const filterButtons = document.querySelectorAll('.filter-btn');
  const searchInput = document.getElementById('lessonSearch');
  const lessonCards = document.querySelectorAll('.lesson-card');
  const noResults = document.getElementById('noResults');

  // Filter by category
  filterButtons.forEach(button => {
    button.addEventListener('click', function() {
      // Update active state
      filterButtons.forEach(btn => btn.classList.remove('active'));
      this.classList.add('active');

      const filterValue = this.dataset.filter;
      filterLessons(filterValue, searchInput.value);
    });
  });

  // Search functionality
  searchInput.addEventListener('input', function() {
    const activeFilter = document.querySelector('.filter-btn.active');
    filterLessons(activeFilter.dataset.filter, this.value);
  });

  function filterLessons(categoryFilter, searchTerm) {
    let visibleCount = 0;
    const searchTermLower = searchTerm.toLowerCase();

    lessonCards.forEach(card => {
      const matchesCategory = categoryFilter === 'all' ||
                            card.dataset.category.includes(categoryFilter);
      const matchesSearch = card.dataset.title.includes(searchTermLower) ||
                          card.dataset.author.includes(searchTermLower);

      if (matchesCategory && matchesSearch) {
        card.style.display = 'block';
        visibleCount++;
      } else {
        card.style.display = 'none';
      }
    });

    // Show/hide no results message
    noResults.style.display = visibleCount === 0 ? 'block' : 'none';

    // Add animation to visible cards
    animateCards();
  }

  function animateCards() {
    const visibleCards = Array.from(lessonCards).filter(
      card => card.style.display !== 'none'
    );

    visibleCards.forEach((card, index) => {
      setTimeout(() => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'all 0.3s ease';

        setTimeout(() => {
          card.style.opacity = '1';
          card.style.transform = 'translateY(0)';
        }, 50);
      }, index * 50);
    });
  }

  // Initial filter
  filterLessons('all', '');
});