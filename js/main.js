document.addEventListener('DOMContentLoaded', () => {
  const scrollBtn = document.querySelector('#scroll-featured');
  const featuredSection = document.querySelector('#featured-art');

  if (scrollBtn && featuredSection) {
    scrollBtn.addEventListener('click', () => {
      featuredSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  }

  document.querySelectorAll('.media-container').forEach(container => {
    const hoverVideoUrl = container.dataset.hoverVideo;
    let video = container.querySelector('video.hover-video');

    if (hoverVideoUrl && !video) {
      video = document.createElement('video');
      video.className = 'hover-video';
      video.src = hoverVideoUrl;
      video.muted = true;
      video.loop = true;
      video.playsInline = true;
      video.preload = 'metadata';
      container.appendChild(video);
    }

    if (!video) {
      return;
    }

    container.classList.add('has-video');
    container.addEventListener('mouseenter', () => {
      video.currentTime = 0;
      video.play().catch(() => {});
    });

    container.addEventListener('mouseleave', () => {
      video.pause();
      video.currentTime = 0;
    });
  });
});
