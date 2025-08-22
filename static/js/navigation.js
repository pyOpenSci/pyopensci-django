/**
 * Navigation functionality for PyOpenSci Django site
 * Handles mobile menu toggle and dropdown menus
 */

document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
            
            // Toggle hamburger icon (optional enhancement)
            const icon = this.querySelector('i');
            icon.classList.toggle('fa-bars');
            icon.classList.toggle('fa-times');
        });
    }
    
    // Mobile dropdown toggles
    const dropdownToggles = document.querySelectorAll('.mobile-dropdown-toggle');
    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', function() {
            const dropdownMenu = this.nextElementSibling;
            const icon = this.querySelector('i');
            const isCurrentlyOpen = !dropdownMenu.classList.contains('hidden');
            
            // Close all other dropdowns first
            dropdownToggles.forEach(otherToggle => {
                if (otherToggle !== toggle) {
                    const otherDropdownMenu = otherToggle.nextElementSibling;
                    const otherIcon = otherToggle.querySelector('i');
                    
                    if (otherDropdownMenu && otherIcon) {
                        otherDropdownMenu.classList.add('hidden');
                        otherIcon.classList.remove('fa-caret-up');
                        otherIcon.classList.add('fa-caret-down');
                    }
                }
            });
            
            // Toggle current dropdown
            if (dropdownMenu && icon) {
                if (isCurrentlyOpen) {
                    dropdownMenu.classList.add('hidden');
                    icon.classList.remove('fa-caret-up');
                    icon.classList.add('fa-caret-down');
                } else {
                    dropdownMenu.classList.remove('hidden');
                    icon.classList.remove('fa-caret-down');
                    icon.classList.add('fa-caret-up');
                }
            }
        });
    });
    
    // Close mobile menu when clicking outside (optional enhancement)
    document.addEventListener('click', function(event) {
        if (mobileMenu && mobileMenuButton) {
            const isClickInsideMenu = mobileMenu.contains(event.target);
            const isClickOnButton = mobileMenuButton.contains(event.target);
            
            if (!isClickInsideMenu && !isClickOnButton && !mobileMenu.classList.contains('hidden')) {
                mobileMenu.classList.add('hidden');
                const icon = mobileMenuButton.querySelector('i');
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        }
    });
});