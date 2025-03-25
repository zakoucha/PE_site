document.addEventListener('DOMContentLoaded', function() {
    // Hero Slider
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
        document.querySelector('.next').addEventListener('click', nextSlide);
        document.querySelector('.prev').addEventListener('click', prevSlide);

        // Auto-advance slides
        function startSlider() {
            slideInterval = setInterval(nextSlide, 5000);
        }

        function pauseSlider() {
            clearInterval(slideInterval);
        }

        // Pause on hover
        const slider = document.querySelector('.hero-slider');
        slider.addEventListener('mouseenter', pauseSlider);
        slider.addEventListener('mouseleave', startSlider);

        startSlider();
        showSlide(0);
    } catch (e) {
        console.error('Slider initialization error:', e);
    }

    // Smooth scrolling for anchor links
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

    // Console greeting
    console.log('%c🏃‍♂️ Physical Education Site Loaded!', 'color: #FF3E41; font-size: 14px;');
});
// Enhanced likeReview function
async function likeReview(reviewId) {
  const likeBtn = document.querySelector(`button[onclick="likeReview(${reviewId})"]`);
  const likeIcon = likeBtn.querySelector('.like-icon');
  const likeCount = likeBtn.querySelector('.like-count');

  // Visual feedback
  likeBtn.disabled = true;
  likeIcon.innerHTML = '<i class="fas fa-spinner fa-pulse"></i>';

  try {
    const response = await fetch(`/lessons/api/reviews/like/${reviewId}/`, {
      method: "POST",
      headers: {
        "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
        "Content-Type": "application/json"
      }
    });

    if (!response.ok) throw new Error('Network error');

    const data = await response.json();

    // Update UI
    likeCount.textContent = data.likes;
    likeBtn.classList.toggle('liked', data.liked);
    likeIcon.innerHTML = '<i class="fas fa-thumbs-up"></i>';

    // Celebration effect for new likes
    if (data.liked) {
      likeIcon.style.transform = 'scale(1.5)';
      setTimeout(() => {
        likeIcon.style.transform = 'scale(1)';
      }, 300);
    }

  } catch (error) {
    console.error('Error:', error);
    likeIcon.innerHTML = '<i class="fas fa-exclamation-circle"></i>';
    setTimeout(() => {
      likeIcon.innerHTML = '<i class="fas fa-thumbs-up"></i>';
    }, 1000);
  } finally {
    likeBtn.disabled = false;
  }
}
// Review form interactivity
document.querySelector('#reviewForm textarea').addEventListener('input', function() {
  const submitBtn = this.closest('form').querySelector('button[type="submit"]');
  const charCount = document.getElementById('charCount');
  const currentLength = this.value.length;

  charCount.textContent = currentLength;
  submitBtn.disabled = currentLength < 10 || currentLength > 500;

  // Visual feedback
  if (currentLength > 450) {
    charCount.classList.add('text-warning');
  } else {
    charCount.classList.remove('text-warning');
  }
});

// Form submission handler
document.querySelector('#reviewForm').addEventListener('submit', function(e) {
  const textarea = this.querySelector('textarea');
  if (textarea.value.length < 10) {
    e.preventDefault();
    textarea.classList.add('is-invalid');
  }
});