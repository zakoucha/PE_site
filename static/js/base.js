document.addEventListener('DOMContentLoaded', function() {
    // =============================================
    // Theme Toggle Functionality
    // =============================================
    const themeToggle = document.getElementById('themeToggle');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');
    const html = document.documentElement;

    function applyTheme(isDark) {
        // Update HTML attribute
        html.setAttribute('data-bs-theme', isDark ? 'dark' : 'light');

        // Update toggle button
        themeToggle.innerHTML = isDark
            ? '<i class="fas fa-sun"></i>'
            : '<i class="fas fa-moon"></i>';
        themeToggle.className = isDark
            ? 'btn btn-sm btn-outline-light'
            : 'btn btn-sm btn-outline-secondary';

        // Save preference
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
    }

    function toggleTheme() {
        const isDark = html.getAttribute('data-bs-theme') === 'dark';
        applyTheme(!isDark);
    }

    // Initialize theme
    function initializeTheme() {
        const storedTheme = localStorage.getItem('theme');
        if (storedTheme) {
            applyTheme(storedTheme === 'dark');
        } else {
            applyTheme(prefersDark.matches);
        }
    }

    // Event listeners
    themeToggle.addEventListener('click', toggleTheme);
    prefersDark.addListener(e => {
        if (!localStorage.getItem('theme')) {
            applyTheme(e.matches);
        }
    });

    // =============================================
    // Hero Slider Functionality
    // =============================================
    try {
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

        // Button event listeners
        document.querySelector('.next')?.addEventListener('click', nextSlide);
        document.querySelector('.prev')?.addEventListener('click', prevSlide);

        // Auto-advance slides
        function startSlider() {
            slideInterval = setInterval(nextSlide, 5000);
        }

        function pauseSlider() {
            clearInterval(slideInterval);
        }

        // Pause on hover
        const slider = document.querySelector('.hero-slider');
        if (slider) {
            slider.addEventListener('mouseenter', pauseSlider);
            slider.addEventListener('mouseleave', startSlider);
            startSlider();
        }

        showSlide(0);
    } catch (e) {
        console.error('Slider initialization error:', e);
    }

    // =============================================
    // Scroll Progress Indicator
    // =============================================
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

    // =============================================
    // Mobile Menu Toggle Animation
    // =============================================
    document.querySelector('.navbar-toggler')?.addEventListener('click', function() {
        this.classList.toggle('active');
        this.innerHTML = this.classList.contains('active')
            ? '<i class="fas fa-times"></i>'
            : '<span class="navbar-toggler-icon"></span>';
    });

    // =============================================
    // Smooth Scrolling for Anchor Links
    // =============================================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // =============================================
    // Initialize Everything
    // =============================================
    initializeTheme();

    // Console greeting
    console.log('%c🏃‍♂️ Physical Education Site Loaded!', 'color: #FF3E41; font-size: 14px;');
});

// Immediate theme initialization to prevent FOUC
(function() {
    const storedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    document.documentElement.setAttribute('data-bs-theme',
        storedTheme ? storedTheme : (prefersDark ? 'dark' : 'light'));
})();