// ScholarDeep - Ultra Modern Dark Mode UI/UX with Advanced Interactions

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all interactive components
    initNavigation();
    initFAQAccordion();
    initTestimonialSlider();
    initInfiniteScrolling();
    initMicroInteractions();
    initParallaxEffects();
    initGlowEffects();
    initCursorEffects();
});

// Mobile Navigation
function initNavigation() {
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');
    const ctaButton = document.querySelector('.cta-button');
    
    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', function() {
            // Create mobile menu if it doesn't exist
            if (!document.querySelector('.mobile-menu')) {
                const mobileMenu = document.createElement('div');
                mobileMenu.className = 'mobile-menu';
                
                // Clone navigation links
                const navLinksClone = navLinks.cloneNode(true);
                mobileMenu.appendChild(navLinksClone);
                
                // Clone CTA button
                if (ctaButton) {
                    const ctaButtonClone = ctaButton.cloneNode(true);
                    mobileMenu.appendChild(ctaButtonClone);
                }
                
                // Add close button
                const closeBtn = document.createElement('div');
                closeBtn.className = 'mobile-menu-close';
                closeBtn.innerHTML = '<i class="fas fa-times"></i>';
                mobileMenu.appendChild(closeBtn);
                
                // Add to DOM
                document.body.appendChild(mobileMenu);
                
                // Add event listener to close button
                closeBtn.addEventListener('click', function() {
                    mobileMenu.classList.remove('active');
                    setTimeout(() => {
                        mobileMenu.remove();
                    }, 300);
                });
                
                // Add event listeners to links for closing menu when clicked
                const mobileLinks = mobileMenu.querySelectorAll('a');
                mobileLinks.forEach(link => {
                    link.addEventListener('click', function() {
                        mobileMenu.classList.remove('active');
                        setTimeout(() => {
                            mobileMenu.remove();
                        }, 300);
                    });
                });
                
                // Animate menu in
                setTimeout(() => {
                    mobileMenu.classList.add('active');
                }, 10);
            } else {
                const mobileMenu = document.querySelector('.mobile-menu');
                mobileMenu.classList.toggle('active');
            }
        });
    }
    
    // Sticky header on scroll
    const header = document.querySelector('header');
    let lastScrollTop = 0;
    
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > 100) {
            header.classList.add('scrolled');
            
            // Hide header when scrolling down, show when scrolling up
            if (scrollTop > lastScrollTop) {
                header.classList.add('hidden');
            } else {
                header.classList.remove('hidden');
            }
        } else {
            header.classList.remove('scrolled');
            header.classList.remove('hidden');
        }
        
        lastScrollTop = scrollTop;
    });
}

// FAQ Accordion
function initFAQAccordion() {
    const faqItems = document.querySelectorAll('.faq-item');
    
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        const toggle = item.querySelector('.faq-toggle');
        
        question.addEventListener('click', function() {
            // Close other open items
            faqItems.forEach(otherItem => {
                if (otherItem !== item && otherItem.classList.contains('active')) {
                    otherItem.classList.remove('active');
                    otherItem.querySelector('.faq-toggle i').className = 'fas fa-plus';
                }
            });
            
            // Toggle current item
            item.classList.toggle('active');
            
            // Change icon
            if (item.classList.contains('active')) {
                toggle.innerHTML = '<i class="fas fa-minus"></i>';
            } else {
                toggle.innerHTML = '<i class="fas fa-plus"></i>';
            }
        });
    });
}

// Testimonial Slider
function initTestimonialSlider() {
    const slider = document.querySelector('.testimonials-slider');
    const dots = document.querySelectorAll('.testimonial-dots .dot');
    const cards = document.querySelectorAll('.testimonial-card');
    let currentIndex = 0;
    let autoSlideInterval;
    
    // Function to update slider position
    function updateSlider(index) {
        // Update current index
        currentIndex = index;
        
        // Calculate position based on viewport
        let position = 0;
        if (window.innerWidth > 768) {
            // Desktop view - show 3 cards at once
            position = index * -33.333;
        } else {
            // Mobile view - show 1 card at a time
            position = index * -100;
        }
        
        // Apply transform
        slider.style.transform = `translateX(${position}%)`;
        
        // Update dots
        dots.forEach((dot, i) => {
            dot.classList.toggle('active', i === index);
        });
    }
    
    // Add click event to dots
    dots.forEach((dot, i) => {
        dot.addEventListener('click', () => {
            updateSlider(i);
            resetAutoSlide();
        });
    });
    
    // Auto slide function
    function startAutoSlide() {
        autoSlideInterval = setInterval(() => {
            let nextIndex = (currentIndex + 1) % dots.length;
            updateSlider(nextIndex);
        }, 5000);
    }
    
    // Reset auto slide timer
    function resetAutoSlide() {
        clearInterval(autoSlideInterval);
        startAutoSlide();
    }
    
    // Touch/swipe support
    let touchStartX = 0;
    let touchEndX = 0;
    
    slider.addEventListener('touchstart', e => {
        touchStartX = e.changedTouches[0].screenX;
    });
    
    slider.addEventListener('touchend', e => {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
    });
    
    function handleSwipe() {
        const swipeThreshold = 50;
        if (touchEndX < touchStartX - swipeThreshold) {
            // Swipe left - next slide
            let nextIndex = (currentIndex + 1) % dots.length;
            updateSlider(nextIndex);
            resetAutoSlide();
        }
        if (touchEndX > touchStartX + swipeThreshold) {
            // Swipe right - previous slide
            let prevIndex = (currentIndex - 1 + dots.length) % dots.length;
            updateSlider(prevIndex);
            resetAutoSlide();
        }
    }
    
    // Initialize auto slide
    startAutoSlide();
    
    // Pause auto slide when hovering over slider
    slider.addEventListener('mouseenter', () => {
        clearInterval(autoSlideInterval);
    });
    
    slider.addEventListener('mouseleave', () => {
        startAutoSlide();
    });
    
    // Handle window resize
    window.addEventListener('resize', () => {
        updateSlider(currentIndex);
    });
}

// Optimized Infinite Scrolling for Feature Cards with reduced lag
function initInfiniteScrolling() {
    const featuresGrid = document.querySelector('.features-grid');
    if (!featuresGrid) return;
    
    // Clone the feature cards for infinite scrolling
    const cards = featuresGrid.querySelectorAll('.feature-card');
    const cardCount = cards.length;
    
    if (cardCount === 0) return;
    
    // Create three columns for the scrolling effect
    const column1 = document.createElement('div');
    column1.className = 'feature-column column-down';
    
    const column2 = document.createElement('div');
    column2.className = 'feature-column column-up';
    
    const column3 = document.createElement('div');
    column3.className = 'feature-column column-down';
    
    // Clear the features grid and add the columns
    featuresGrid.innerHTML = '';
    featuresGrid.appendChild(column1);
    featuresGrid.appendChild(column2);
    featuresGrid.appendChild(column3);
    
    // Distribute cards among columns - use fewer cards per column to reduce DOM elements
    const cardsPerColumn = Math.min(Math.ceil(cardCount / 3), 4); // Limit to max 4 cards per column
    
    // Function to create a card set with performance optimizations
    function createCardSet(startIdx, count, column) {
        const container = document.createElement('div');
        container.className = 'cards-container';
        
        // Add original cards
        for (let i = 0; i < count; i++) {
            const idx = (startIdx + i) % cardCount;
            const card = cards[idx].cloneNode(true);
            // Add will-change to optimize rendering performance
            card.style.willChange = 'transform';
            container.appendChild(card);
        }
        
        // Add clone cards for seamless loop - only clone what's needed
        for (let i = 0; i < count; i++) {
            const idx = (startIdx + i) % cardCount;
            const card = cards[idx].cloneNode(true);
            card.style.willChange = 'transform';
            container.appendChild(card);
        }
        
        column.appendChild(container);
        
        // Add hover effect to cards with performance optimizations
        const allCards = container.querySelectorAll('.feature-card');
        allCards.forEach(card => {
            // Use a single class toggle instead of direct style manipulation
            card.addEventListener('mouseenter', () => {
                // Pause animation on hover
                container.classList.add('paused');
                card.classList.add('card-hover');
            });
            
            card.addEventListener('mouseleave', () => {
                // Resume animation
                container.classList.remove('paused');
                card.classList.remove('card-hover');
            });
        });
    }
    
    // Create card sets for each column
    createCardSet(0, cardsPerColumn, column1);
    createCardSet(cardsPerColumn, cardsPerColumn, column2);
    createCardSet(cardsPerColumn * 2, Math.min(cardCount - (cardsPerColumn * 2), cardsPerColumn), column3);
    
    // Apply CSS for the scrolling effect with performance optimizations
    const style = document.createElement('style');
    style.textContent = `
        .features-grid {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 2rem;
            overflow: hidden;
            position: relative;
            z-index: 1;
        }
        
        .feature-column {
            display: flex;
            flex-direction: column;
            gap: 2rem;
            overflow: hidden;
            height: 800px; /* Reduced height */
            position: relative;
        }
        
        .cards-container {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            display: flex;
            flex-direction: column;
            gap: 2rem;
            animation-duration: 60s; /* Slower animation for better performance */
            animation-timing-function: linear;
            animation-iteration-count: infinite;
            will-change: transform; /* Optimize for animations */
        }
        
        .cards-container.paused {
            animation-play-state: paused;
        }
        
        .column-up .cards-container {
            animation-name: scrollUp;
        }
        
        .column-down .cards-container {
            animation-name: scrollDown;
        }
        
        .card-hover {
            transform: translateY(-15px) scale(1.05) !important;
            z-index: 10;
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3), 0 0 20px rgba(139, 92, 246, 0.3) !important;
        }
        
        @media (max-width: 768px) {
            .features-grid {
                grid-template-columns: 1fr;
            }
            
            .feature-column:not(.column-up) {
                display: none;
            }
        }
    `;
    
    document.head.appendChild(style);
    
    // Use IntersectionObserver instead of scroll event for better performance
    const featuresSection = document.getElementById('features');
    if (featuresSection) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                // Only adjust animation when features section is visible
                if (entry.isIntersecting) {
                    // Set a fixed animation speed instead of continuously adjusting
                    const containers = document.querySelectorAll('.cards-container');
                    containers.forEach(container => {
                        container.style.animationDuration = '60s';
                    });
                }
            });
        }, { threshold: 0.1 }); // Trigger when at least 10% of the section is visible
        
        observer.observe(featuresSection);
    }
}

// Advanced Micro Interactions
function initMicroInteractions() {
    // Button hover effects with magnetic pull
    const buttons = document.querySelectorAll('.btn');
    
    buttons.forEach(button => {
        // Magnetic effect
        button.addEventListener('mousemove', function(e) {
            const rect = this.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            // Calculate distance from center
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            // Calculate pull strength (stronger when closer to button)
            const pull = 0.2;
            const moveX = (x - centerX) * pull;
            const moveY = (y - centerY) * pull;
            
            // Apply transform
            this.style.transform = `translate(${moveX}px, ${moveY}px)`;
        });
        
        // Reset position when mouse leaves
        button.addEventListener('mouseleave', function() {
            this.style.transform = '';
        });
        
        // Create ripple effect on mouseenter
        button.addEventListener('mouseenter', function(e) {
            // Create ripple effect
            const ripple = document.createElement('span');
            ripple.className = 'btn-ripple';
            this.appendChild(ripple);
            
            // Position the ripple at mouse position
            const rect = button.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            ripple.style.left = `${x}px`;
            ripple.style.top = `${y}px`;
            
            // Remove ripple after animation
            setTimeout(() => {
                ripple.remove();
            }, 1000);
            
            // Add glow effect
            const glow = document.createElement('span');
            glow.className = 'btn-glow';
            this.appendChild(glow);
            
            // Remove glow after animation
            setTimeout(() => {
                glow.remove();
            }, 1000);
        });
    });
    
    // Add icons to buttons that don't have them
    const primaryButtons = document.querySelectorAll('.primary-btn');
    primaryButtons.forEach(button => {
        if (!button.querySelector('i')) {
            const buttonText = button.textContent.trim();
            let iconClass = 'fa-arrow-right';
            
            // Choose icon based on button text
            if (buttonText.toLowerCase().includes('search')) {
                iconClass = 'fa-search';
            } else if (buttonText.toLowerCase().includes('start')) {
                iconClass = 'fa-rocket';
            } else if (buttonText.toLowerCase().includes('learn')) {
                iconClass = 'fa-book';
            } else if (buttonText.toLowerCase().includes('find')) {
                iconClass = 'fa-compass';
            }
            
            button.innerHTML = `<i class="fas ${iconClass}"></i> ${buttonText}`;
        }
    });
    
    const secondaryButtons = document.querySelectorAll('.secondary-btn');
    secondaryButtons.forEach(button => {
        if (!button.querySelector('i')) {
            const buttonText = button.textContent.trim();
            let iconClass = 'fa-info-circle';
            
            // Choose icon based on button text
            if (buttonText.toLowerCase().includes('learn')) {
                iconClass = 'fa-graduation-cap';
            } else if (buttonText.toLowerCase().includes('more')) {
                iconClass = 'fa-plus-circle';
            }
            
            button.innerHTML = `<i class="fas ${iconClass}"></i> ${buttonText}`;
        }
    });
    
    // Add hover effect style
    const style = document.createElement('style');
    style.textContent = `
        .btn-ripple {
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.5);
            transform: scale(0);
            animation: ripple 1s cubic-bezier(0.19, 1, 0.22, 1);
            pointer-events: none;
            z-index: 1;
        }
        
        .btn-glow {
            position: absolute;
            inset: -5px;
            border-radius: 16px;
            background: var(--gradient-5);
            opacity: 0;
            z-index: -1;
            filter: blur(10px);
            animation: glow 1s cubic-bezier(0.19, 1, 0.22, 1);
            pointer-events: none;
        }
        
        @keyframes ripple {
            to {
                transform: scale(6);
                opacity: 0;
            }
        }
        
        @keyframes glow {
            0% {
                opacity: 0;
                filter: blur(10px);
            }
            50% {
                opacity: 0.5;
                filter: blur(15px);
            }
            100% {
                opacity: 0;
                filter: blur(20px);
            }
        }
        
        .mobile-menu {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: var(--bg-primary);
            z-index: 2000;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            gap: 2rem;
            opacity: 0;
            visibility: hidden;
            transition: all 0.3s ease;
        }
        
        .mobile-menu.active {
            opacity: 1;
            visibility: visible;
        }
        
        .mobile-menu .nav-links {
            display: flex;
            flex-direction: column;
            gap: 2rem;
            text-align: center;
        }
        
        .mobile-menu .nav-links a {
            font-size: 1.5rem;
        }
        
        .mobile-menu-close {
            position: absolute;
            top: 2rem;
            right: 2rem;
            font-size: 2rem;
            cursor: pointer;
            color: var(--text-primary);
        }
        
        header.scrolled {
            background: rgba(10, 12, 16, 0.95);
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
        }
        
        header.hidden {
            transform: translateY(-100%);
        }
    `;
    
    document.head.appendChild(style);
}

// Parallax Effects
function initParallaxEffects() {
    // Add parallax effect to sections
    window.addEventListener('scroll', function() {
        const scrollPosition = window.pageYOffset;
        
        // Hero section parallax
        const hero = document.querySelector('.hero');
        if (hero) {
            hero.style.backgroundPositionY = `${scrollPosition * 0.5}px`;
        }
        
        // Animate elements when they come into view
        const animateElements = document.querySelectorAll('.feature-card, .step, .testimonial-card, .faq-item');
        
        animateElements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;
            
            if (elementPosition < windowHeight * 0.85) {
                element.classList.add('animate-in');
            }
        });
    });
    
    // Add animation styles
    const style = document.createElement('style');
    style.textContent = `
        .feature-card, .step, .testimonial-card, .faq-item {
            opacity: 0;
            transform: translateY(30px);
            transition: opacity 0.6s ease, transform 0.6s ease;
        }
        
        .animate-in {
            opacity: 1;
            transform: translateY(0);
        }
    `;
    
    document.head.appendChild(style);
    
    // Trigger initial check
    setTimeout(() => {
        window.dispatchEvent(new Event('scroll'));
    }, 100);
}

// Advanced Glow Effects
function initGlowEffects() {
    // Create floating glow orbs that move around the page
    const glowContainer = document.createElement('div');
    glowContainer.className = 'glow-container';
    document.body.appendChild(glowContainer);
    
    // Create multiple glow orbs
    for (let i = 0; i < 5; i++) {
        const orb = document.createElement('div');
        orb.className = 'glow-orb';
        
        // Random size
        const size = Math.random() * 200 + 100;
        orb.style.width = `${size}px`;
        orb.style.height = `${size}px`;
        
        // Random position
        orb.style.left = `${Math.random() * 100}vw`;
        orb.style.top = `${Math.random() * 100}vh`;
        
        // Random color from our palette
        const colors = [
            'rgba(139, 92, 246, 0.15)', // Purple
            'rgba(59, 130, 246, 0.15)', // Blue
            'rgba(236, 72, 153, 0.15)', // Pink
            'rgba(16, 185, 129, 0.15)', // Green
            'rgba(245, 158, 11, 0.15)'  // Orange
        ];
        orb.style.background = colors[Math.floor(Math.random() * colors.length)];
        
        // Add to container
        glowContainer.appendChild(orb);
        
        // Animate the orb
        animateOrb(orb);
    }
    
    // Function to animate orbs
    function animateOrb(orb) {
        // Random duration
        const duration = Math.random() * 60 + 30;
        
        // Random movement
        const keyframes = [
            { transform: `translate(0, 0) scale(1)`, opacity: 0.5 },
            { 
                transform: `translate(${Math.random() * 40 - 20}vw, ${Math.random() * 40 - 20}vh) scale(${Math.random() * 0.5 + 0.8})`, 
                opacity: Math.random() * 0.3 + 0.2 
            },
            { 
                transform: `translate(${Math.random() * 40 - 20}vw, ${Math.random() * 40 - 20}vh) scale(${Math.random() * 0.5 + 0.8})`, 
                opacity: Math.random() * 0.3 + 0.2 
            },
            { transform: `translate(0, 0) scale(1)`, opacity: 0.5 }
        ];
        
        // Apply animation
        orb.animate(keyframes, {
            duration: duration * 1000,
            iterations: Infinity,
            easing: 'cubic-bezier(0.25, 0.1, 0.25, 1)'
        });
    }
    
    // Add styles
    const style = document.createElement('style');
    style.textContent = `
        .glow-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            pointer-events: none;
            z-index: -1;
            overflow: hidden;
        }
        
        .glow-orb {
            position: absolute;
            border-radius: 50%;
            filter: blur(50px);
            opacity: 0.3;
            mix-blend-mode: screen;
        }
        
        .glow-effect-1, .glow-effect-2 {
            position: fixed;
            border-radius: 50%;
            filter: blur(100px);
            opacity: 0.15;
            mix-blend-mode: screen;
            pointer-events: none;
            z-index: -1;
        }
        
        .glow-effect-1 {
            width: 60vw;
            height: 60vw;
            background: radial-gradient(circle, rgba(139, 92, 246, 0.5), transparent 70%);
            top: -20vw;
            right: -20vw;
            animation: float1 20s infinite alternate ease-in-out;
        }
        
        .glow-effect-2 {
            width: 50vw;
            height: 50vw;
            background: radial-gradient(circle, rgba(59, 130, 246, 0.5), transparent 70%);
            bottom: -20vw;
            left: -10vw;
            animation: float2 25s infinite alternate ease-in-out;
        }
        
        @keyframes float1 {
            0% { transform: translate(0, 0); }
            100% { transform: translate(10vw, 10vh); }
        }
        
        @keyframes float2 {
            0% { transform: translate(0, 0); }
            100% { transform: translate(-5vw, -10vh); }
        }
    `;
    
    document.head.appendChild(style);
}

// Custom Cursor Effects - Simplified to just a dot
function initCursorEffects() {
    // Create custom cursor dot element
    const cursorDot = document.createElement('div');
    cursorDot.className = 'cursor-dot';
    document.body.appendChild(cursorDot);
    
    // Track mouse movement with optimized performance
    let mouseX = 0;
    let mouseY = 0;
    let dotX = 0;
    let dotY = 0;
    
    // Use requestAnimationFrame for smoother performance
    function animateDot() {
        // Add some smoothing for natural movement
        const speed = 0.2;
        dotX += (mouseX - dotX) * speed;
        dotY += (mouseY - dotY) * speed;
        
        cursorDot.style.left = `${dotX}px`;
        cursorDot.style.top = `${dotY}px`;
        
        requestAnimationFrame(animateDot);
    }
    
    // Start animation loop
    animateDot();
    
    // Update mouse position with throttled event listener
    let isThrottled = false;
    document.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
        
        // Apply immediate position on initial movement
        if (dotX === 0 && dotY === 0) {
            dotX = mouseX;
            dotY = mouseY;
        }
    });
    
    // Add hover effect for interactive elements
    const interactiveElements = document.querySelectorAll('a, button, .btn, .feature-card, .faq-item, .nav-link');
    
    interactiveElements.forEach(element => {
        element.addEventListener('mouseenter', () => {
            cursorDot.classList.add('dot-hover');
        });
        
        element.addEventListener('mouseleave', () => {
            cursorDot.classList.remove('dot-hover');
        });
    });
    
    // Add click effect
    document.addEventListener('mousedown', () => {
        cursorDot.classList.add('dot-click');
    });
    
    document.addEventListener('mouseup', () => {
        cursorDot.classList.remove('dot-click');
    });
    
    // Add styles
    const style = document.createElement('style');
    style.textContent = `
        body {
            cursor: none;
        }
        
        .cursor-dot {
            position: fixed;
            width: 10px;
            height: 10px;
            background-color: rgba(139, 92, 246, 1);
            border-radius: 50%;
            pointer-events: none;
            transform: translate(-50%, -50%);
            z-index: 10000;
            transition: transform 0.1s, width 0.2s, height 0.2s, background-color 0.2s;
            box-shadow: 0 0 10px rgba(139, 92, 246, 0.5);
        }
        
        .dot-hover {
            width: 14px;
            height: 14px;
            background-color: rgba(236, 72, 153, 1);
            transform: translate(-50%, -50%) scale(1.2);
        }
        
        .dot-click {
            width: 8px;
            height: 8px;
            background-color: rgba(16, 185, 129, 1);
            transform: translate(-50%, -50%) scale(0.8);
        }
        
        @media (max-width: 768px) {
            .cursor-dot {
                display: none;
            }
            
            body {
                cursor: auto;
            }
        }
    `;
    
    document.head.appendChild(style);
}