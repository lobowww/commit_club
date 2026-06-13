// CommitClub - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    const menuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (menuBtn && mobileMenu) {
        menuBtn.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }

    // Auto-dismiss messages after 5 seconds
    const messages = document.querySelectorAll('.alert-message');
    messages.forEach(function(msg) {
        setTimeout(function() {
            msg.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            msg.style.opacity = '0';
            msg.style.transform = 'translateY(-10px)';
            setTimeout(function() { msg.remove(); }, 500);
        }, 5000);
    });

    // Animate numbers on scroll
    const counters = document.querySelectorAll('[data-count]');
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                const target = entry.target;
                const count = parseInt(target.getAttribute('data-count'));
                animateCounter(target, 0, count, 1500);
                observer.unobserve(target);
            }
        });
    }, { threshold: 0.5 });

    counters.forEach(function(counter) { observer.observe(counter); });

    // Counter animation
    function animateCounter(element, start, end, duration) {
        let startTime = null;
        function step(timestamp) {
            if (!startTime) startTime = timestamp;
            const progress = Math.min((timestamp - startTime) / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 3); // easeOutCubic
            element.textContent = Math.floor(eased * (end - start) + start);
            if (progress < 1) {
                requestAnimationFrame(step);
            } else {
                element.textContent = end.toLocaleString('pt-BR');
            }
        }
        requestAnimationFrame(step);
    }

    // Progress bars animation
    const progressBars = document.querySelectorAll('.progress-fill');
    const progressObserver = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                const bar = entry.target;
                const width = bar.getAttribute('data-width');
                setTimeout(function() {
                    bar.style.width = width + '%';
                }, 200);
                progressObserver.unobserve(bar);
            }
        });
    }, { threshold: 0.3 });

    progressBars.forEach(function(bar) { progressObserver.observe(bar); });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

    // Page enter animation
    const mainContent = document.querySelector('main');
    if (mainContent) {
        mainContent.classList.add('page-enter');
    }
});
