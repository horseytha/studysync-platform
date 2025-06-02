// Mobile Navigation Toggle
document.addEventListener('DOMContentLoaded', function() {
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            navToggle.classList.toggle('active');
        });
    }
    
    // Smooth scrolling for anchor links
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
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
    
    // Add scroll effect to navbar
    window.addEventListener('scroll', function() {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 50) {
            navbar.style.backgroundColor = 'rgba(139, 21, 56, 0.95)';
        } else {
            navbar.style.backgroundColor = '';
        }
    });

    // Initialize 3D Carousel
    initializeCarousel();
});

// 3D Carousel Functionality
let currentSlide = 0;
const totalSlides = 6;
const radius = 400; // Distance from center
const angleStep = 360 / totalSlides;

function initializeCarousel() {
    updateCarouselPositions();

    // Auto-rotate carousel every 5 seconds
    setInterval(() => {
        moveCarousel(1);
    }, 5000);
}

function updateCarouselPositions() {
    const slides = document.querySelectorAll('.feature-slide');
    const track = document.querySelector('.carousel-track');

    // Rotate the entire track
    const trackRotation = currentSlide * -angleStep;
    track.style.transform = `rotateY(${trackRotation}deg)`;

    slides.forEach((slide, index) => {
        const angle = index * angleStep;
        const isActive = index === currentSlide;

        // Calculate circular 3D position
        const rotateY = angle;
        const translateZ = -radius;
        const opacity = isActive ? 1 : 0.6;
        const scale = isActive ? 1 : 0.85;

        // Position each slide in a circle
        slide.style.transform = `
            rotateY(${rotateY}deg)
            translateZ(${translateZ}px)
            scale(${scale})
        `;

        slide.style.opacity = opacity;

        // Update active class
        slide.classList.toggle('active', isActive);
    });

    // Update indicators
    updateIndicators();
}

function moveCarousel(direction) {
    currentSlide = (currentSlide + direction + totalSlides) % totalSlides;
    updateCarouselPositions();
}

function goToSlide(slideIndex) {
    currentSlide = slideIndex;
    updateCarouselPositions();
}

function updateIndicators() {
    const indicators = document.querySelectorAll('.indicator');
    indicators.forEach((indicator, index) => {
        indicator.classList.toggle('active', index === currentSlide);
    });
}
