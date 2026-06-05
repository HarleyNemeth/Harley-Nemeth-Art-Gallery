document.addEventListener('DOMContentLoaded', () => {
    const navItems = [
        { label: 'Home', href: '/', icon: 'fa-house', key: '' },
        { label: 'Store', href: '/store/', icon: 'fa-store', key: 'store' },
        { label: 'Gallery', href: '/gallery/', icon: 'fa-images', key: 'gallery' },
        { label: 'Contact', href: '/contact/', icon: 'fa-envelope', key: 'contact' },
        { label: 'Cart', href: '/cart/', icon: 'fa-shopping-cart', key: 'cart' }
    ]

    const currentPath = window.location.pathname
    const logoSrc = '/static/images/HN_logo.png'

    const navHtml = `
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <div class="container-fluid ps-4 pe-4">
                <a class="navbar-brand d-flex align-items-center" href="/">
                    <img src="${logoSrc}" alt="Nemeth Art Logo" class="logo me-2">
                </a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#mainNavbar" aria-controls="mainNavbar" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="mainNavbar">
                    <ul class="navbar-nav ms-auto mb-2 mb-lg-0 gap-3">
                        ${navItems.map(item => `
                            <li class="nav-item">
                                <a class="nav-link${currentPath === item.href ? ' active' : ''}" href="${item.href}">
                                    <i class="fa-solid ${item.icon}"></i> ${item.label}
                                </a>
                            </li>
                        `).join('')}
                    </ul>
                </div>
            </div>
        </nav>
    `

    const header = document.querySelector('#site-header')
    if (header) {
        header.innerHTML = navHtml

        const navbarToggler = header.querySelector('.navbar-toggler')
        const navbarCollapse = header.querySelector('.navbar-collapse')

        if (navbarToggler && navbarCollapse) {
            const collapse = new bootstrap.Collapse(navbarCollapse, {
                toggle: false
            })

            navbarToggler.addEventListener('click', () => {
                collapse.toggle()
            })

            header.querySelectorAll('.nav-link').forEach(link => {
                link.addEventListener('click', () => {
                    collapse.hide()
                })
            })
        }
    }
})