// حذف modal-backdrop بعد از بستن مودال
document.addEventListener('hidden.bs.modal', function () {
    document.querySelectorAll('.modal-backdrop').forEach(function (backdrop) {
        backdrop.remove();
    });
    document.body.classList.remove('modal-open');
    document.body.style.overflow = 'auto';
    // توقف پخش ویدئو هنگام بستن مودال
    document.querySelectorAll('.modal video').forEach(function (video) {
        video.pause();
        video.currentTime = 0;
    });
});

// نمایش پیام‌های Django پس از لود صفحه
document.addEventListener('DOMContentLoaded', function () {
    {% for message in messages %}
        showNotification("{{ message | escapejs }}", 10000);
    {% endfor %}
});

// اصلاح خطا: استفاده از ID صحیح برای SVG
const svg = document.getElementById('arrows');
const xPoint = document.getElementById('xPoint');
const services = document.querySelectorAll('.service-text');
const particlesContainer = document.getElementById('particles');

// جلوگیری از هدایت به صفحه توضیحات هنگام کلیک روی ویدئو
document.querySelectorAll('.card-img-top').forEach(video => {
    video.addEventListener('click', function (e) {
        e.preventDefault(); // جلوگیری از رفتار پیش‌فرض لینک
        e.stopPropagation(); // جلوگیری از انتشار رویداد به والد
    });
});

// Create floating light particles
function createParticles() {
    const particleCount = 30;
    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        const posX = Math.random() * 100;
        const posY = Math.random() * 100;
        const size = Math.random() * 3 + 1;
        const delay = Math.random() * 10;
        const duration = Math.random() * 10 + 10;
        particle.style.left = `${posX}%`;
        particle.style.top = `${posY}%`;
        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;
        particle.style.animationDelay = `${delay}s`;
        particle.style.animationDuration = `${duration}s`;
        particlesContainer.appendChild(particle);
    }
}

// Create light particles along the path
function createPathParticles(path, count) {
    const pathLength = path.getTotalLength();
    const particles = [];
    for (let i = 0; i < count; i++) {
        const particle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        particle.setAttribute('r', Math.random() * 2 + 1);
        particle.setAttribute('class', 'path-particle');
        const point = path.getPointAtLength(0);
        particle.setAttribute('cx', point.x);
        particle.setAttribute('cy', point.y);
        svg.appendChild(particle);
        particles.push({
            element: particle,
            position: Math.random(),
            speed: Math.random() * 0.01 + 0.005,
            delay: Math.random() * 1000
        });
    }
    return { pathLength, particles };
}

// Animate particles along the path
function animatePathParticles(path, pathInfo) {
    const { pathLength, particles } = pathInfo;
    particles.forEach(particle => {
        setTimeout(() => {
            const duration = 1500 + Math.random() * 500;
            let start = null;
            function step(timestamp) {
                if (!start) start = timestamp;
                const progress = (timestamp - start) / duration;
                if (progress < 1) {
                    const currentPosition = Math.min(progress, 1);
                    const point = path.getPointAtLength(currentPosition * pathLength);
                    particle.element.setAttribute('cx', point.x);
                    particle.element.setAttribute('cy', point.y);
                    const fadeProgress = progress * 3 % 1;
                    let opacity = fadeProgress < 0.5 ? fadeProgress * 2 : (1 - fadeProgress) * 2;
                    particle.element.style.opacity = opacity;
                    requestAnimationFrame(step);
                } else {
                    particle.element.remove();
                }
            }
            requestAnimationFrame(step);
        }, particle.delay);
    });
}

// رسم فلش‌ها
function drawSequentialArrows() {
    svg.innerHTML = '';
    const svgRect = svg.getBoundingClientRect();
    const xPointRect = xPoint.getBoundingClientRect();
    const startX = xPointRect.left + xPointRect.width / 2 - svgRect.left;
    const startY = xPointRect.top + xPointRect.height / 2 - svgRect.top;

    const animationDuration = 1200;
    const delayBetweenArrows = 300;
    const animations = [
        'webReveal 1.2s cubic-bezier(0.23, 1, 0.32, 1) forwards',
        'telegramReveal 1.2s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards',
        'tradingReveal 1.2s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards'
    ];

    services.forEach((service, index) => {
        const rect = service.getBoundingClientRect();
        const endX = rect.left + rect.width / 2 - svgRect.left;
        const endY = rect.top + rect.height / 2 - svgRect.top;

        setTimeout(() => {
            const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
            const d = `M${startX},${startY} C${startX},${startY + 80} ${endX},${endY - 120} ${endX},${endY}`;
            path.setAttribute('d', d);
            path.setAttribute('class', 'connection-path');
            path.style.animation = 'drawLine 1.2s ease-in-out forwards';

            const arrowHead = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
            const size = 8;
            const arrowPoints = `${endX},${endY} ${endX - size},${endY - size} ${endX + size},${endY - size}`;
            arrowHead.setAttribute('points', arrowPoints);
            arrowHead.setAttribute('class', 'arrow-head');
            arrowHead.style.animation = 'fadeInArrow 0.5s ease-in forwards 0.7s';

            svg.appendChild(path);
            svg.appendChild(arrowHead);

            const particleCount = 8 + Math.round(Math.random() * 5);
            const pathInfo = createPathParticles(path, particleCount);

            setTimeout(() => {
                animatePathParticles(path, pathInfo);
            }, 300);

            setTimeout(() => {
                service.style.animation = animations[index];
            }, 700);
        }, index * (animationDuration + delayBetweenArrows));
    });
}

// اجرای انیمیشن‌ها پس از بارگذاری فونت‌ها
document.fonts.ready.then(() => {
    createParticles();
    requestAnimationFrame(() => {
        drawSequentialArrows();
    });
});

// مدیریت تغییر اندازه صفحه
let resizeTimeout;
window.addEventListener('resize', () => {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(() => {
        drawSequentialArrows();
    }, 250);
});

// Animated Cards Interaction
document.addEventListener('DOMContentLoaded', function() {
    const cards = document.querySelectorAll('.service-card');
    
    cards.forEach(card => {
        // Mouse move animation
        card.addEventListener('mousemove', (e) => {
            const x = e.clientX - card.getBoundingClientRect().left;
            const y = e.clientY - card.getBoundingClientRect().top;
            
            const centerX = card.offsetWidth / 2;
            const centerY = card.offsetHeight / 2;
            
            const angleX = (y - centerY) / 20;
            const angleY = (centerX - x) / 20;
            
            card.style.transform = `perspective(1000px) rotateX(${angleX}deg) rotateY(${angleY}deg) scale(1.05)`;
            
            // Parallax effect for image
            const image = card.querySelector('.card-image img');
            const posX = (centerX - x) / 20;
            const posY = (centerY - y) / 20;
            image.style.transform = `translateX(${posX}px) translateY(${posY}px)`;
            
            // Glow effect
            const glowColor = card.classList.contains('web-design-card') ? 'rgba(78, 154, 241, 0.3)' :
                             card.classList.contains('telegram-bot-card') ? 'rgba(42, 171, 238, 0.3)' :
                             'rgba(50, 205, 50, 0.3)';
            
            card.style.boxShadow = `${-angleY * 2}px ${angleX * 2}px 30px ${glowColor}`;
        });
        
        // Mouse leave animation
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale(1)';
            card.style.boxShadow = '0 25px 45px rgba(0, 0, 0, 0.1)';
            
            const image = card.querySelector('.card-image img');
            image.style.transform = 'translateX(0) translateY(0)';
        });
        
        // Click animation
        card.addEventListener('click', () => {
            card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale(0.98)';
            setTimeout(() => {
                card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale(1.03)';
            }, 100);
        });
    });
    
    // Add floating particles to the section background
    const animatedServices = document.getElementById('animated-services');
    for (let i = 0; i < 20; i++) {
        const particle = document.createElement('div');
        particle.className = 'floating-particle';
        
        // Random position
        const posX = Math.random() * 100;
        const posY = Math.random() * 100;
        
        // Random size
        const size = Math.random() * 6 + 2;
        
        // Random animation duration and delay
        const duration = Math.random() * 20 + 10;
        const delay = Math.random() * 5;
        
        // Random color
        const colors = ['rgba(100, 255, 200, 0.3)', 'rgba(150, 100, 255, 0.3)', 'rgba(255, 100, 200, 0.3)'];
        const color = colors[Math.floor(Math.random() * colors.length)];
        
        particle.style.left = `${posX}%`;
        particle.style.top = `${posY}%`;
        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;
        particle.style.background = color;
        particle.style.animationDuration = `${duration}s`;
        particle.style.animationDelay = `${delay}s`;
        
        animatedServices.appendChild(particle);
    }
});

// function showNotification(message, duration = 10000) {
//     const container = document.getElementById('notificationContainer');
    
//     // Create notification element
//     const notification = document.createElement('div');
//     notification.className = 'notification';
//     notification.innerHTML = `
//         <button class="notification-close">×</button>
//         <div class="notification-message">${message}</div>
//         <div class="notification-progress">
//             <div class="notification-progress-bar" style="transition-duration: ${duration}ms"></div>
//         </div>
//     `;
    
//     // Add to container
//     container.appendChild(notification);
    
//     // Trigger animation
//     setTimeout(() => notification.classList.add('show'), 10);
    
//     // Start progress bar
//     setTimeout(() => {
//         const progressBar = notification.querySelector('.notification-progress-bar');
//         progressBar.style.width = '0%';
//     }, 50);
    
//     // Close button functionality
//     const closeBtn = notification.querySelector('.notification-close');
//     closeBtn.addEventListener('click', () => {
//         removeNotification(notification);
//     });
    
//     // Auto-remove after duration
//     const timer = setTimeout(() => {
//         removeNotification(notification);
//     }, duration);
    
//     // Function to remove notification
//     function removeNotification(notificationElement) {
//         clearTimeout(timer);
//         notificationElement.classList.remove('show');
//         setTimeout(() => {
//             notificationElement.remove();
//         }, 300);
//     }
// }

// For your portfolio items, you might want to add notifications when clicking items
document.querySelectorAll('.btn-neon').forEach(button => {
    button.addEventListener('click', function() {
        const portfolioTitle = this.closest('.card-body')?.querySelector('.card-title')?.textContent;
        if (portfolioTitle) {
            showNotification(`Viewing details for: ${portfolioTitle}`, 10000);
        }
    });
});


document.addEventListener('DOMContentLoaded', function() {
// Service Carousel Implementation
const carousel = document.querySelector('.service-carousel');
const slides = document.querySelectorAll('.service-slide');
const dots = document.querySelectorAll('.dot');
const prevArrow = document.querySelector('.prev-arrow');
const nextArrow = document.querySelector('.next-arrow');

let currentIndex = 0;
let isAnimating = false;
const totalSlides = slides.length;
const animationDuration = 800; // Match CSS transition duration

// Initialize carousel
function initCarousel() {
    slides.forEach((slide, index) => {
        slide.classList.remove('active', 'prev', 'next');
        
        if (index === currentIndex) {
            slide.classList.add('active');
        } else if (index === (currentIndex - 1 + totalSlides) % totalSlides) {
            slide.classList.add('prev');
        } else if (index === (currentIndex + 1) % totalSlides) {
            slide.classList.add('next');
        }
    });
    
    updateDots();
    isAnimating = false;
}

// Update navigation dots
function updateDots() {
    dots.forEach((dot, index) => {
        dot.classList.toggle('active', index === currentIndex);
    });
}

// Go to specific slide
function goToSlide(index) {
    if (isAnimating) return;
    
    isAnimating = true;
    currentIndex = (index + totalSlides) % totalSlides;
    initCarousel();
}

// Go to next slide
function nextSlide() {
    if (isAnimating) return;
    
    isAnimating = true;
    currentIndex = (currentIndex + 1) % totalSlides;
    initCarousel();
}

// Go to previous slide
function prevSlide() {
    if (isAnimating) return;
    
    isAnimating = true;
    currentIndex = (currentIndex - 1 + totalSlides) % totalSlides;
    initCarousel();
}

// Event listeners for arrows
nextArrow.addEventListener('click', nextSlide);
prevArrow.addEventListener('click', prevSlide);

// Event listeners for dots
dots.forEach(dot => {
    dot.addEventListener('click', function() {
        const slideIndex = parseInt(this.getAttribute('data-index'));
        if (slideIndex !== currentIndex) {
            goToSlide(slideIndex);
        }
    });
});

// Keyboard navigation
document.addEventListener('keydown', function(e) {
    if (e.key === 'ArrowRight') {
        nextSlide();
    } else if (e.key === 'ArrowLeft') {
        prevSlide();
    }
});

// Touch/swipe support
let touchStartX = 0;
let touchEndX = 0;
const swipeThreshold = 50;

carousel.addEventListener('touchstart', function(e) {
    touchStartX = e.changedTouches[0].screenX;
}, {passive: true});

carousel.addEventListener('touchend', function(e) {
    touchEndX = e.changedTouches[0].screenX;
    handleSwipe();
}, {passive: true});

function handleSwipe() {
    const difference = touchStartX - touchEndX;
    
    if (difference > swipeThreshold) {
        nextSlide();
    } else if (difference < -swipeThreshold) {
        prevSlide();
    }
}

// Auto-rotation (optional)
let autoRotateInterval;
const autoRotateDelay = 5000; // 5 seconds

function startAutoRotate() {
    autoRotateInterval = setInterval(nextSlide, autoRotateDelay);
}

function stopAutoRotate() {
    clearInterval(autoRotateInterval);
}

// Pause auto-rotate on hover/touch
carousel.addEventListener('mouseenter', stopAutoRotate);
carousel.addEventListener('mouseleave', startAutoRotate);
carousel.addEventListener('touchstart', stopAutoRotate, {passive: true});
carousel.addEventListener('touchend', startAutoRotate, {passive: true});

// Initialize everything
initCarousel();
startAutoRotate();

// Add smooth transitions when images load
const carouselImages = document.querySelectorAll('.card-image img');
carouselImages.forEach(img => {
    if (img.complete) {
        img.style.transition = 'transform 0.5s ease';
    } else {
        img.addEventListener('load', function() {
            this.style.transition = 'transform 0.5s ease';
        });
    }
});

// Accessibility improvements
slides.forEach((slide, index) => {
    slide.setAttribute('aria-hidden', index !== currentIndex);
    slide.setAttribute('aria-label', `Service ${index + 1}`);
});

prevArrow.setAttribute('aria-label', 'Previous service');
nextArrow.setAttribute('aria-label', 'Next service');

dots.forEach(dot => {
    dot.setAttribute('aria-label', `Go to service ${parseInt(dot.getAttribute('data-index')) + 1}`);
});
});