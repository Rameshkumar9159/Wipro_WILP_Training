/* Navigation Enhancement Script for Storage Systems Documentation
   Author: T S Rameshkumar
   Batch: WiproNGA_Datacentre_B9_25VID2182
   Purpose: Enhance navigation functionality and ensure subtopics remain visible */

(function() {
    'use strict';
    
    // Wait for DOM to be fully loaded
    document.addEventListener('DOMContentLoaded', function() {
        console.log('Navigation enhancement script loaded');
        
        // Function to expand all navigation items on page load
        function expandAllNavigationItems() {
            const navItems = document.querySelectorAll('.wy-menu-vertical li');
            navItems.forEach(function(item) {
                item.classList.add('current');
                item.setAttribute('aria-expanded', 'true');
            });
        }
        
        // Function to ensure proper current page highlighting
        function highlightCurrentPage() {
            const currentUrl = window.location.pathname;
            const navLinks = document.querySelectorAll('.wy-menu-vertical a');
            
            navLinks.forEach(function(link) {
                const linkPath = new URL(link.href).pathname;
                if (linkPath === currentUrl) {
                    link.closest('li').classList.add('current-page');
                    link.style.fontWeight = 'bold';
                    link.style.backgroundColor = '#e7f2fa';
                    link.style.borderLeft = '3px solid #2980b9';
                }
            });
        }
        
        // Function to improve expand/collapse button functionality
        function enhanceExpandButtons() {
            const expandButtons = document.querySelectorAll('button.toctree-expand');
            
            expandButtons.forEach(function(button) {
                button.addEventListener('click', function(e) {
                    e.stopPropagation();
                    const parentLi = button.closest('li');
                    const nestedUl = parentLi.querySelector('ul');
                    
                    if (nestedUl) {
                        const isExpanded = !nestedUl.style.display || nestedUl.style.display === 'block';
                        nestedUl.style.display = isExpanded ? 'none' : 'block';
                        button.setAttribute('aria-expanded', !isExpanded);
                        
                        // Update icon
                        if (isExpanded) {
                            button.innerHTML = '+';
                            button.title = 'Expand section';
                        } else {
                            button.innerHTML = '−';
                            button.title = 'Collapse section';
                        }
                    }
                });
            });
        }
        
        // Function to add smooth scrolling to navigation links
        function addSmoothScrolling() {
            const navLinks = document.querySelectorAll('.wy-menu-vertical a[href^="#"]');
            
            navLinks.forEach(function(link) {
                link.addEventListener('click', function(e) {
                    const targetId = link.getAttribute('href').substring(1);
                    const targetElement = document.getElementById(targetId);
                    
                    if (targetElement) {
                        e.preventDefault();
                        targetElement.scrollIntoView({
                            behavior: 'smooth',
                            block: 'start'
                        });
                        
                        // Update URL without triggering page reload
                        history.pushState(null, null, '#' + targetId);
                    }
                });
            });
        }
        
        // Initialize all enhancements
        setTimeout(function() {
            expandAllNavigationItems();
            highlightCurrentPage();
            enhanceExpandButtons();
            addSmoothScrolling();
            
            console.log('Navigation enhancements applied successfully');
        }, 100);
        
        // Re-apply enhancements when navigation changes (for dynamic content)
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === 'childList' && mutation.target.classList.contains('wy-menu-vertical')) {
                    setTimeout(function() {
                        enhanceExpandButtons();
                        highlightCurrentPage();
                    }, 50);
                }
            });
        });
        
        const navigationContainer = document.querySelector('.wy-menu-vertical');
        if (navigationContainer) {
            observer.observe(navigationContainer, {
                childList: true,
                subtree: true
            });
        }
    });
    
    // Add custom styles for enhanced navigation
    const style = document.createElement('style');
    style.textContent = `
        /* Enhanced navigation styles */
        .wy-menu-vertical li.current-page > a {
            background-color: #e7f2fa !important;
            border-left: 3px solid #2980b9 !important;
            font-weight: bold !important;
        }
        
        .wy-menu-vertical button.toctree-expand {
            font-family: monospace !important;
            font-size: 12px !important;
            width: 16px !important;
            height: 16px !important;
            text-align: center !important;
            line-height: 14px !important;
        }
        
        .wy-menu-vertical a {
            transition: all 0.2s ease !important;
        }
        
        .wy-menu-vertical a:hover {
            transform: translateX(2px) !important;
        }
    `;
    document.head.appendChild(style);
    
})();
