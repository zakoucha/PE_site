document.addEventListener('DOMContentLoaded', function() {
    // =============================================
    // Theme Toggling
    // =============================================
    const themeToggle = document.getElementById('themeToggle');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');
    const html = document.documentElement;

    function applyTheme(isDark) {
        html.setAttribute('data-bs-theme', isDark ? 'dark' : 'light');
        themeToggle.innerHTML = isDark
            ? '<i class="fas fa-sun"></i>'
            : '<i class="fas fa-moon"></i>';
        themeToggle.className = isDark
            ? 'btn btn-sm btn-outline-light'
            : 'btn btn-sm btn-outline-secondary';
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
    }

    function toggleTheme() {
        const isDark = html.getAttribute('data-bs-theme') === 'dark';
        applyTheme(!isDark);
    }

    function initializeTheme() {
        const storedTheme = localStorage.getItem('theme');
        if (storedTheme) {
            applyTheme(storedTheme === 'dark');
        } else {
            applyTheme(prefersDark.matches);
        }
    }

    themeToggle?.addEventListener('click', toggleTheme);
    prefersDark.addListener(e => {
        if (!localStorage.getItem('theme')) {
            applyTheme(e.matches);
        }
    });

    // =============================================
    // Dropdown Menu Handling
    // =============================================
    function setupDropdowns() {
        // Initialize Bootstrap dropdowns
        const dropdowns = document.querySelectorAll('[data-bs-toggle="dropdown"]');
        dropdowns.forEach(dropdown => new bootstrap.Dropdown(dropdown));

        // Submenu handling
        document.querySelectorAll('.dropdown-submenu').forEach(el => {
            const toggle = el.querySelector('.dropdown-toggle');
            const menu = el.querySelector('.dropdown-menu');

            // Mobile click handling
            toggle?.addEventListener('click', (e) => {
                if (window.innerWidth <= 991) {
                    e.preventDefault();
                    e.stopPropagation();
                    menu.classList.toggle('show');

                    // Close other submenus
                    document.querySelectorAll('.dropdown-submenu .dropdown-menu').forEach(otherMenu => {
                        if (otherMenu !== menu && otherMenu.classList.contains('show')) {
                            otherMenu.classList.remove('show');
                        }
                    });
                }
            });

            // Desktop hover handling
            if (window.innerWidth > 991) {
                el?.addEventListener('mouseenter', () => menu.classList.add('show'));
                el?.addEventListener('mouseleave', () => menu.classList.remove('show'));
            }
        });
    }

    // =============================================
    // Hero Slider (Vanilla JS Version)
    // =============================================
    function setupSlider() {
        const slides = document.querySelectorAll('.slide');
        const nextBtn = document.querySelector('.slider-control.next');
        const prevBtn = document.querySelector('.slider-control.prev');
        let currentSlide = 0;
        let sliderInterval;

        function showSlide(index) {
            slides.forEach(slide => slide.classList.remove('active-slide'));
            slides[index]?.classList.add('active-slide');
        }

        function nextSlide() {
            currentSlide = (currentSlide + 1) % slides.length;
            showSlide(currentSlide);
        }

        function prevSlide() {
            currentSlide = (currentSlide - 1 + slides.length) % slides.length;
            showSlide(currentSlide);
        }

        function startAutoSlide() {
            sliderInterval = setInterval(nextSlide, 5000);
        }

        function stopAutoSlide() {
            clearInterval(sliderInterval);
        }

        if (slides.length > 0) {
            showSlide(0);
            startAutoSlide();

            // Event listeners
            nextBtn?.addEventListener('click', nextSlide);
            prevBtn?.addEventListener('click', prevSlide);

            const slider = document.querySelector('.hero-slider');
            slider?.addEventListener('mouseenter', stopAutoSlide);
            slider?.addEventListener('mouseleave', startAutoSlide);
        }
    }

    // =============================================
    // Scroll Progress Indicator
    // =============================================
    function setupScrollProgress() {
        window.addEventListener('scroll', () => {
            const scrollTop = document.documentElement.scrollTop;
            const scrollHeight = document.documentElement.scrollHeight;
            const clientHeight = document.documentElement.clientHeight;
            const progress = (scrollTop / (scrollHeight - clientHeight)) * 100;
            document.querySelector('.scroll-progress')?.style.width = `${progress}%`;
        });
    }

    // =============================================
    // Mobile Menu Toggle
    // =============================================
    document.querySelector('.navbar-toggler')?.addEventListener('click', function() {
        this.classList.toggle('active');
        this.innerHTML = this.classList.contains('active')
            ? '<i class="fas fa-times"></i>'
            : '<span class="navbar-toggler-icon"></span>';
    });

    // =============================================
    // Initialize All Components
    // =============================================
    initializeTheme();
    setupDropdowns();
    setupSlider();
    setupScrollProgress();

    // Console greeting
    console.log('%c🏃‍♂️ Physical Education Site Loaded!', 'color: #FF3E41; font-size: 14px;');
});

// Immediate theme initialization to prevent FOUC
(function() {
    const storedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    document.documentElement.setAttribute('data-bs-theme',
        storedTheme ? storedTheme : (prefersDark ? 'dark' : 'light')
    );
})();