document.addEventListener('DOMContentLoaded', () => {
  const isRoot = !window.location.pathname.includes('/html/');
  const homeHref = isRoot ? 'index.html' : '../index.html';
  const pageBase = isRoot ? 'html/' : '';
  const navItems = [
    { label: 'Home', href: homeHref, icon: 'fa-house', key: 'index.html' },
    { label: 'Store', href: isRoot ? 'html/store.html' : 'store.html', icon: 'fa-store', key: 'store.html' },
    { label: 'Gallery', href: isRoot ? 'html/gallery.html' : 'gallery.html', icon: 'fa-images', key: 'gallery.html' },
    { label: 'Contact', href: isRoot ? 'html/contact.html' : 'contact.html', icon: 'fa-envelope', key: 'contact.html' },
    { label: 'Cart', href: isRoot ? 'html/cart.html' : 'cart.html', icon: 'fa-shopping-cart', key: 'cart.html' }
  ];

  const currentPage = window.location.pathname.split('/').pop() || 'index.html';
  const brandLink = homeHref;

  const navHtml = `
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container-fluid ps-4 pe-4">
        <a class="navbar-brand d-flex align-items-center" href="${brandLink}">
          <img src="${isRoot ? 'images/HN_logo.png' : '../images/HN_logo.png'}" alt="Nemeth Art Logo" class="logo me-2">
        </a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#mainNavbar" aria-controls="mainNavbar" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="mainNavbar">
          <ul class="navbar-nav ms-auto mb-2 mb-lg-0 gap-3">
            ${navItems.map(item => `
              <li class="nav-item">
                <a class="nav-link${item.key === currentPage ? ' active' : ''}" href="${item.href}">
                  <i class="fa-solid ${item.icon}"></i>${item.label}
                </a>
              </li>
            `).join('')}
          </ul>
        </div>
      </div>
    </nav>
  `;

  const header = document.querySelector('#site-header');
  if (header) {
    header.innerHTML = navHtml;
    
    // Initialize Bootstrap collapse for the dynamically created navbar
    const navbarToggler = header.querySelector('.navbar-toggler');
    const navbarCollapse = header.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
      const collapse = new bootstrap.Collapse(navbarCollapse, {
        toggle: false
      });
      
      navbarToggler.addEventListener('click', () => {
        collapse.toggle();
      });
      
      // Close navbar when a link is clicked
      const navLinks = header.querySelectorAll('.nav-link');
      navLinks.forEach(link => {
        link.addEventListener('click', () => {
          collapse.hide();
        });
      });
    }
  }
});
