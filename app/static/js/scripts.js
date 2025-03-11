// Custom JavaScript for handling UI interactions
document.addEventListener('DOMContentLoaded', function() {
    // Get the mobile toggle button and navigation
    const mobileToggle = document.querySelector('.mobile-toggle');
    const mainNav = document.querySelector('.main-nav');
    
    // Add click event to toggle button
    if (mobileToggle && mainNav) {
      mobileToggle.addEventListener('click', function() {
        mainNav.classList.toggle('active');
      });
    }
    
    // Handle window resize
    window.addEventListener('resize', function() {
      if (window.innerWidth > 768 && mainNav) {
        mainNav.classList.remove('active');
      }
    });
  });