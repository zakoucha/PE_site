document.addEventListener('DOMContentLoaded', function() {
    // =============================================
    // Theme Toggle Functionality
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

    themeToggle.addEventListener('click', toggleTheme);
    prefersDark.addListener(e => {
        if (!localStorage.getItem('theme')) {
            applyTheme(e.matches);
        }
    });

    // =============================================
    // Dropdown Menu Fixes
    // =============================================
    function setupDropdowns() {
        // Initialize all dropdowns
        var dropdownElements = [].slice.call(document.querySelectorAll('[data-bs-toggle="dropdown"]'));
        dropdownElements.forEach(function (dropdownToggleEl) {
            new bootstrap.Dropdown(dropdownToggleEl);
        });

        // Handle submenu behavior
        document.querySelectorAll('.dropdown-submenu').forEach(function(el) {
            const toggle = el.querySelector('.dropdown-toggle');
            const menu = el.querySelector('.dropdown-menu');

            // Click handler for mobile
            toggle.addEventListener('click', function(e) {
                if (window.innerWidth <= 991) {
                    e.preventDefault();
                    e.stopPropagation();
                    menu.classList.toggle('show');

                    // Close other open submenus
                    document.querySelectorAll('.dropdown-submenu .dropdown-menu').forEach(function(otherMenu) {
                        if (otherMenu !== menu && otherMenu.classList.contains('show')) {
                            otherMenu.classList.remove('show');
                        }
                    });
                }
            });

            // Hover handler for desktop
            if (window.innerWidth > 991) {
                el.addEventListener('mouseenter', function() {
                    menu.classList.add('show');
                });

                el.addEventListener('mouseleave', function() {
                    menu.classList.remove('show');
                });
            }
        });
    }

    // =============================================
    // Hero Slider Functionality
    // =============================================
    function setupSlider() {
        let currentSlide = 0;
        const slides = document.querySelectorAll('.slide');
        const totalSlides = slides.length;
        let slideInterval;

        function showSlide(index) {
            slides.forEach(slide => slide.classList.remove('active'));
            slides[index].classList.add('active');
        }

        function nextSlide() {
            currentSlide = (currentSlide + 1) % totalSlides;
            showSlide(currentSlide);
        }

        function prevSlide() {
            currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
            showSlide(currentSlide);
        }

        document.querySelector('.next')?.addEventListener('click', nextSlide);
        document.querySelector('.prev')?.addEventListener('click', prevSlide);

        function startSlider() {
            slideInterval = setInterval(nextSlide, 5000);
        }

        function pauseSlider() {
            clearInterval(slideInterval);
        }

        const slider = document.querySelector('.hero-slider');
        if (slider) {
            slider.addEventListener('mouseenter', pauseSlider);
            slider.addEventListener('mouseleave', startSlider);
            startSlider();
        }

        showSlide(0);
    }

    // =============================================
    // Scroll Progress Indicator
    // =============================================
    function setupScrollProgress() {
        window.addEventListener('scroll', function() {
            const scrollTop = document.documentElement.scrollTop;
            const scrollHeight = document.documentElement.scrollHeight;
            const clientHeight = document.documentElement.clientHeight;
            const progress = (scrollTop / (scrollHeight - clientHeight)) * 100;
            const progressBar = document.querySelector('.scroll-progress');
            if (progressBar) {
                progressBar.style.width = progress + '%';
            }
        });
    }

    // =============================================
    // Initialize Everything
    // =============================================
    initializeTheme();
    setupDropdowns();
    setupSlider();
    setupScrollProgress();

    // Mobile menu toggle animation
    document.querySelector('.navbar-toggler')?.addEventListener('click', function() {
        this.classList.toggle('active');
        this.innerHTML = this.classList.contains('active')
            ? '<i class="fas fa-times"></i>'
            : '<span class="navbar-toggler-icon"></span>';
    });

    // Console greeting
    console.log('%c🏃‍♂️ Physical Education Site Loaded!', 'color: #FF3E41; font-size: 14px;');
});

// Immediate theme initialization to prevent FOUC
(function() {
    const storedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    document.documentElement.setAttribute('data-bs-theme',
        storedTheme ? storedTheme