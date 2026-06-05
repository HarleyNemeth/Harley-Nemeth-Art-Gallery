document.addEventListener('DOMContentLoaded', () => {
  const socialLinks = [
    { platform: 'Instagram', icon: 'fa-instagram', handle: 'harley.nemeth', url: 'https://www.instagram.com/harley.nemeth/' },
    { platform: 'LinkedIn', icon: 'fa-linkedin', handle: 'harley-nemeth', url: 'https://www.linkedin.com/in/harley-nemeth-b25212306' },
    { platform: 'TikTok', icon: 'fa-tiktok', handle: '@harleynemethart', url: 'https://www.tiktok.com/@harleynemethart' },
    { platform: 'YouTube', icon: 'fa-youtube', handle: 'Harley Nemeth', url: 'https://www.youtube.com/@Harley_Nemeth' }
  ];

  const footerHtml = `
    <div class="container-fluid py-4">
      <div class="row align-items-center justify-content-center gy-3">
        <div class="col-12 col-md-auto">
          <div class="social">
            ${socialLinks.map(link => `
              <a href="${link.url}" target="_blank" title="${link.platform}" class="social-icon">
                <i class="fa-brands ${link.icon}"></i>
              </a>
              <a href="${link.url}" target="_blank" title="${link.platform}" class="social-text">
                ${link.handle}
              </a>
            `).join('')}
          </div>
        </div>
      </div>
      <div class="row mt-3">
        <div class="col-12 text-center">
          <p class="mb-0"><i class="fa-solid fa-palette"></i> &copy; 2026 Nemeth Art</p>
        </div>
      </div>
    </div>
  `;

  const footer = document.querySelector('#site-footer');
  if (footer) {
    footer.innerHTML = footerHtml;
  }
});
