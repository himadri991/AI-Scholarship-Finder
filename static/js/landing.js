// ScholarDeep - Ultra Modern Dark Mode UI/UX with Advanced Interactions

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all interactive components
    initNavigation();
    initFAQAccordion();
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
            // Always keep header visible
            header.classList.remove('hidden');
        } else {
            header.classList.remove('scrolled');
            header.classList.remove('hidden');
        }
        
        lastScrollTop = scrollTop;
    });
    
    // Add mobile menu styles
    const style = document.createElement('style');
    style.textContent = `
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
            transform: translateY(0);
            opacity: 1;
        }
    `;
    
    document.head.appendChild(style);
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

// Enhanced Infinite Scrolling for Feature Cards
function initInfiniteScrolling() {
    const featuresGrid = document.querySelector('.features-grid');
    if (!featuresGrid) return;
    
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
    
    // Distribute cards among columns
    const cardsPerColumn = Math.ceil(cardCount / 3);
    
    // Function to create a card set with performance optimizations
    function createCardSet(startIdx, count, column) {
        const container = document.createElement('div');
        container.className = 'cards-container';
        
        // Add original cards
        for (let i = 0; i < count; i++) {
            const idx = (startIdx + i) % cardCount;
            const card = cards[idx].cloneNode(true);
            container.appendChild(card);
        }
        
        // Add duplicate cards for seamless loop
        for (let i = 0; i < count; i++) {
            const idx = (startIdx + i) % cardCount;
            const card = cards[idx].cloneNode(true);
            container.appendChild(card);
        }
        
        column.appendChild(container);
        
        // Add hover effect to pause animation
        const allCards = container.querySelectorAll('.feature-card');
        allCards.forEach(card => {
            card.addEventListener('mouseenter', () => {
                container.classList.add('paused');
            });
            
            card.addEventListener('mouseleave', () => {
                container.classList.remove('paused');
            });
        });
    }
    
    // Create card sets for each column
    createCardSet(0, cardsPerColumn, column1);
    createCardSet(cardsPerColumn, cardsPerColumn, column2);
    createCardSet(cardsPerColumn * 2, Math.min(cardCount - (cardsPerColumn * 2), cardsPerColumn), column3);
}

// Advanced Micro Interactions with Fixed Text Visibility
function initMicroInteractions() {
    // Button hover effects with magnetic pull
    const buttons = document.querySelectorAll('.btn');
    
    buttons.forEach(button => {
        // Ensure text and icons are always visible
        const text = button.textContent || button.innerText;
        const icon = button.querySelector('i');
        
        // Magnetic effect
        button.addEventListener('mousemove', function(e) {
            const rect = this.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            // Calculate distance from center
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            // Calculate pull strength (stronger when closer to button)
            const pull = 0.1;
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
                if (ripple.parentNode) {
                    ripple.remove();
                }
            }, 1000);
        });
    });
    
    // Add hover effect style
    const style = document.createElement('style');
    style.textContent = `
        .btn-ripple {
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.3);
            transform: scale(0);
            animation: ripple 1s cubic-bezier(0.19, 1, 0.22, 1);
            pointer-events: none;
            z-index: 1;
            width: 20px;
            height: 20px;
        }
        
        @keyframes ripple {
            to {
                transform: scale(6);
                opacity: 0;
            }
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
        const animateElements = document.querySelectorAll('.feature-card, .step, .faq-item');
        
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
        .feature-card, .step, .faq-item {
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
    for (let i = 0; i < 3; i++) {
        const orb = document.createElement('div');
        orb.className = 'glow-orb';
        
        // Random size
        const size = Math.random() * 150 + 100;
        orb.style.width = `${size}px`;
        orb.style.height = `${size}px`;
        
        // Random position
        orb.style.left = `${Math.random() * 100}vw`;
        orb.style.top = `${Math.random() * 100}vh`;
        
        // Random color from our palette
        const colors = [
            'rgba(139, 92, 246, 0.1)',
            'rgba(59, 130, 246, 0.1)',
            'rgba(236, 72, 153, 0.1)'
        ];
        orb.style.background = colors[i % colors.length];
        
        // Add to container
        glowContainer.appendChild(orb);
        
        // Animate the orb
        animateOrb(orb);
    }
    
    // Function to animate orbs
    function animateOrb(orb) {
        // Random duration
        const duration = Math.random() * 40 + 30;
        
        // Random movement
        const keyframes = [
            { transform: `translate(0, 0) scale(1)`, opacity: 0.3 },
            { 
                transform: `translate(${Math.random() * 30 - 15}vw, ${Math.random() * 30 - 15}vh) scale(${Math.random() * 0.3 + 0.8})`, 
                opacity: Math.random() * 0.2 + 0.1 
            },
            { transform: `translate(0, 0) scale(1)`, opacity: 0.3 }
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
            filter: blur(60px);
            opacity: 0.2;
            mix-blend-mode: screen;
        }
    `;
    
    document.head.appendChild(style);
}

// Custom Cursor Effects
function initCursorEffects() {
    // Only apply cursor effects on desktop
    if (window.innerWidth <= 768) return;
    
    // Create custom cursor dot element
    const cursorDot = document.createElement('div');
    cursorDot.className = 'cursor-dot';
    document.body.appendChild(cursorDot);
    
    // Track mouse movement
    let mouseX = 0;
    let mouseY = 0;
    let dotX = 0;
    let dotY = 0;
    
    // Use requestAnimationFrame for smoother performance
    function animateDot() {
        // Add smoothing for natural movement
        const speed = 0.15;
        dotX += (mouseX - dotX) * speed;
        dotY += (mouseY - dotY) * speed;
        
        cursorDot.style.left = `${dotX}px`;
        cursorDot.style.top = `${dotY}px`;
        
        requestAnimationFrame(animateDot);
    }
    
    // Start animation loop
    animateDot();
    
    // Update mouse position
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
    const interactiveElements = document.querySelectorAll('a, button, .btn, .feature-card, .faq-item');
    
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
            width: 8px;
            height: 8px;
            background-color: rgba(139, 92, 246, 0.8);
            border-radius: 50%;
            pointer-events: none;
            transform: translate(-50%, -50%);
            z-index: 10000;
            transition: width 0.2s, height 0.2s, background-color 0.2s;
            box-shadow: 0 0 10px rgba(139, 92, 246, 0.3);
        }
        
        .dot-hover {
            width: 12px;
            height: 12px;
            background-color: rgba(236, 72, 153, 0.8);
        }
        
        .dot-click {
            width: 6px;
            height: 6px;
            background-color: rgba(16, 185, 129, 0.8);
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
