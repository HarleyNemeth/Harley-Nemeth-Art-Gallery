document.addEventListener('DOMContentLoaded', function() {
  const scrollBtn = document.getElementById('scroll-featured');
  const featuredSection = document.getElementById('featured-art');

  if (scrollBtn && featuredSection) {
    scrollBtn.addEventListener('click', function() {
      featuredSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  }

  const navLinks = document.querySelectorAll('.nav a');
  const currentPage = window.location.pathname.split('/').pop() || 'index.html';

  navLinks.forEach(function(link) {
    const href = link.getAttribute('href');
    if (!href) return;

    const targetPage = href.split('/').pop() || 'index.html';
    if (targetPage === currentPage) {
      link.classList.add('active');
    } else {
      link.classList.remove('active');
    }
  });

  // Hover video: play on enter, pause/reset on leave
  const mediaContainers = document.querySelectorAll('.media-container');
  mediaContainers.forEach(container => {
    const video = container.querySelector('video.hover-video');
    if (!video) return;

    container.addEventListener('mouseenter', () => {
      try {
        video.currentTime = 0;
        const p = video.play();
        if (p && typeof p.catch === 'function') p.catch(() => {});
      } catch (e) {}
    });

    container.addEventListener('mouseleave', () => {
      try {
        video.pause();
        video.currentTime = 0;
      } catch (e) {}
    });
  });
});
