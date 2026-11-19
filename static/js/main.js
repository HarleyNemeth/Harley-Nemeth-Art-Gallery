gsap.registerPlugin(ScrollTrigger)

document.addEventListener('DOMContentLoaded', () => {

    const commissionGallery = document.querySelector('.commission-gallery')
    if (commissionGallery && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        const commissionArtwork = commissionGallery.querySelectorAll('[data-commission-artwork]')
        gsap.fromTo(
            commissionArtwork,
            { autoAlpha: 0, y: 22 },
            {
                autoAlpha: 1,
                y: 0,
                duration: 0.65,
                stagger: 0.1,
                ease: 'power2.out',
                scrollTrigger: {
                    trigger: commissionGallery,
                    start: 'top 85%',
                    once: true
                }
            }
        )
    }

    const banner = document.querySelector('.banner-container')
    if (banner) {
        const bannerHeight = banner.offsetHeight
        const imgHeight = 160
        const total = bannerHeight + imgHeight * 2
        const leftPositions = [5, 18, 30, 42, 54, 66, 78, 88]
        let scrollDir = -1

        document.querySelectorAll('.float-img').forEach((img, i) => {
            const duration = 7 + Math.random() * 8
            const opacity = 0.5 + Math.random() * 0.5
            const startY = -(imgHeight + Math.random() * bannerHeight)

            gsap.set(img, {
                opacity: opacity,
                left: `${leftPositions[i % leftPositions.length]}%`,
                y: startY
            })

            let currentY = startY

            gsap.ticker.add(() => {
                const speed = (total / (duration * 60)) * scrollDir
                currentY += speed
                if (currentY < -imgHeight) currentY += total
                if (currentY > bannerHeight + imgHeight) currentY -= total
                const progress = (currentY + imgHeight) / total
                const scale = 0.65 + (1 -progress) * 0.5
                const fade = 0.2 + (1 - progress) * 1.2 * opacity
                gsap.set(img, { y: currentY, scale: scale, opacity: fade, transformOrigin: "center bottom" })
            })
        })

        ScrollTrigger.create({
            trigger: "body",
            start: "top top",
            end: "bottom bottom",
            onUpdate: (self) => {
                scrollDir = self.direction === 1 ? -1 : 1
            }
        })
    }

    // Scroll to featured button
    const scrollBtn = document.querySelector('#scroll-featured')
    const featuredSection = document.querySelector('#featured-art')
    if (scrollBtn && featuredSection) {
        scrollBtn.addEventListener('click', () => {
            featuredSection.scrollIntoView({ behavior: 'smooth', block: 'start' })
        })
    }

    // Hover video on gallery cards
    document.querySelectorAll('.media-container').forEach(container => {
        const hoverVideoUrl = container.dataset.hoverVideo
        let video = container.querySelector('video.hover-video')

        if (hoverVideoUrl && !video) {
            video = document.createElement('video')
            video.className = 'hover-video'
            video.src = hoverVideoUrl
            video.muted = true
            video.loop = true
            video.playsInline = true
            video.preload = 'metadata'
            container.appendChild(video)
        }

        if (!video) return

        container.classList.add('has-video')
        container.addEventListener('mouseenter', () => {
            video.currentTime = 0
            video.play().catch(() => {})
        })
        container.addEventListener('mouseleave', () => {
            video.pause()
            video.currentTime = 0
        })
    })


// Shop filtering
const filterBtns = document.querySelectorAll('.filter-btn')
const artItems = document.querySelectorAll('.art-item')

filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        filterBtns.forEach(b => b.classList.remove('active'))
        btn.classList.add('active')
        filterBtns.forEach(b => b.setAttribute('aria-pressed', b === btn ? 'true' : 'false'))

        const filter = btn.dataset.filter

        artItems.forEach(item => {
            const category = item.dataset.category
            const show = filter === 'all' || category === filter

            if (show) {
                gsap.to(item, { opacity: 1, duration: 0.3, onStart: () => item.style.display = 'block' })
            } else {
                gsap.to(item, { opacity: 0, duration: 0.3, onComplete: () => item.style.display = 'none' })
            }
        })

        if (detailsOverlay && !detailsOverlay.hidden && filter !== 'all' && activeCard?.dataset.category !== filter) {
            closeDetails()
        }
    })
})

const shop = document.querySelector('.shop-page')
const detailsOverlay = document.querySelector('.art-details-overlay')
const detailsPanel = document.querySelector('.art-details-panel')
const detailsContent = document.querySelector('.art-details-panel-content')
const mobileDetails = window.matchMedia('(max-width: 767px)')
let activeTrigger = null
let activeCard = null
let savedScrollY = 0
let previousBodyStyles = null

if (shop && detailsOverlay && detailsPanel && detailsContent) {
    const closeButton = detailsPanel.querySelector('.art-details-close')

    const positionDetailsPanel = () => {
        if (!activeCard || mobileDetails.matches) return

        const cardRect = activeCard.getBoundingClientRect()
        const edge = 16
        const minimumWidth = 320
        const maximumWidth = 420
        const viewportWidth = document.documentElement.clientWidth
        const peerRects = Array.from(shop.querySelectorAll('.art-item'))
            .filter(card => card !== activeCard && card.getClientRects().length > 0)
            .map(card => card.getBoundingClientRect())
            .filter(rect => rect.top < cardRect.bottom && rect.bottom > cardRect.top)
        const leftBlocker = peerRects
            .filter(rect => rect.right <= cardRect.left)
            .reduce((nearest, rect) => Math.max(nearest, rect.right), 0)
        const rightBlocker = peerRects
            .filter(rect => rect.left >= cardRect.right)
            .reduce((nearest, rect) => Math.min(nearest, rect.left), viewportWidth)
        const leftSpace = Math.max(0, cardRect.left - edge - (leftBlocker ? leftBlocker + edge : edge))
        const rightSpace = Math.max(0, (rightBlocker === viewportWidth ? viewportWidth - edge : rightBlocker - edge) - cardRect.right - edge)
        const availableSpace = Math.max(leftSpace, rightSpace)

        detailsOverlay.classList.remove('is-left', 'is-right', 'is-centered')
        if (availableSpace < minimumWidth) {
            detailsOverlay.classList.add('is-centered')
            detailsPanel.style.removeProperty('width')
            detailsPanel.style.removeProperty('left')
            detailsPanel.style.removeProperty('right')
            detailsPanel.style.removeProperty('top')
            return
        }

        const width = Math.min(maximumWidth, availableSpace)
        const opensLeft = leftSpace >= rightSpace
        detailsOverlay.classList.add(opensLeft ? 'is-left' : 'is-right')
        detailsPanel.style.width = `${width}px`
        detailsPanel.style.left = opensLeft ? `${cardRect.left - edge - width}px` : 'auto'
        detailsPanel.style.right = opensLeft ? 'auto' : `${viewportWidth - cardRect.right - edge - width}px`
        detailsPanel.style.top = `${Math.max(edge, cardRect.top)}px`

        const panelRect = detailsPanel.getBoundingClientRect()
        const top = Math.max(
            edge,
            Math.min(cardRect.top, window.innerHeight - panelRect.height - edge)
        )
        detailsPanel.style.top = `${top}px`
    }

    const restoreBodyStyles = () => {
        if (!previousBodyStyles) return
        document.body.style.overflow = previousBodyStyles.bodyOverflow
        document.documentElement.style.overflow = previousBodyStyles.documentOverflow
        previousBodyStyles = null
        window.scrollTo(0, savedScrollY)
    }

    const closeDetails = () => {
        if (detailsOverlay.hidden) return
        detailsOverlay.hidden = true
        detailsOverlay.classList.remove(
            'is-visible',
            'is-left',
            'is-right',
            'is-centered',
            'is-mobile'
        )
        detailsPanel.style.removeProperty('width')
        detailsPanel.style.removeProperty('left')
        detailsPanel.style.removeProperty('right')
        detailsPanel.style.removeProperty('top')
        detailsContent.replaceChildren()
        document.body.classList.remove('art-details-open')
        restoreBodyStyles()
        if (activeTrigger) {
            activeTrigger.setAttribute('aria-expanded', 'false')
            activeTrigger.focus()
        }
        activeTrigger = null
        activeCard = null
    }

    const openDetails = trigger => {
        const card = trigger.closest('.art-item')
        const template = card?.querySelector('.art-details-template')
        if (!card || !template) return

        activeTrigger = trigger
        activeCard = card
        savedScrollY = window.scrollY
        previousBodyStyles = {
            bodyOverflow: document.body.style.overflow,
            documentOverflow: document.documentElement.style.overflow
        }
        document.body.style.overflow = 'hidden'
        document.documentElement.style.overflow = 'hidden'

        detailsContent.replaceChildren(template.content.cloneNode(true))
        detailsPanel.setAttribute(
            'aria-labelledby',
            detailsContent.querySelector('.art-details-title') ? 'art-details-title' : 'art-details-panel'
        )
        detailsOverlay.hidden = false
        detailsOverlay.classList.toggle('is-mobile', mobileDetails.matches)
        trigger.setAttribute('aria-expanded', 'true')
        document.body.classList.add('art-details-open')
        positionDetailsPanel()
        window.requestAnimationFrame(() => {
            detailsOverlay.classList.add('is-visible')
            closeButton.focus()
        })
    }

    shop.querySelectorAll('[data-details-trigger]').forEach(trigger => {
        trigger.addEventListener('click', () => openDetails(trigger))
    })

    detailsOverlay.addEventListener('click', event => {
        if (event.target === detailsOverlay) closeDetails()
    })
    closeButton.addEventListener('click', closeDetails)

    detailsPanel.addEventListener('click', event => {
        const thumbnail = event.target.closest('.art-details-thumbnail')
        if (!thumbnail || !detailsPanel.contains(thumbnail)) return

        const thumbnailImage = thumbnail.querySelector('img')
        if (!thumbnailImage) return

        let mainImage = detailsPanel.querySelector('.art-details-main-image')
        if (!mainImage) {
            mainImage = document.createElement('img')
            mainImage.className = 'art-details-main-image'
            mainImage.alt = detailsContent.querySelector('.art-details-title')?.textContent || ''
            detailsPanel.querySelector('.art-details-main-placeholder')?.replaceWith(mainImage)
        }
        mainImage.setAttribute('src', thumbnailImage.getAttribute('src'))

        detailsPanel.querySelectorAll('.art-details-thumbnail').forEach(button => {
            const isSelected = button === thumbnail
            button.classList.toggle('is-active', isSelected)
            button.setAttribute('aria-pressed', isSelected ? 'true' : 'false')
        })
    })

    document.addEventListener('keydown', event => {
        if (detailsOverlay.hidden) return
        if (event.key === 'Escape') {
            event.preventDefault()
            closeDetails()
            return
        }
        if (event.key !== 'Tab') return

        const focusable = Array.from(detailsPanel.querySelectorAll(
            'button:not([disabled]), a[href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'
        ))
        if (!focusable.length) {
            event.preventDefault()
            detailsPanel.focus()
            return
        }
        const first = focusable[0]
        const last = focusable[focusable.length - 1]
        if (event.shiftKey && document.activeElement === first) {
            event.preventDefault()
            last.focus()
        } else if (!event.shiftKey && document.activeElement === last) {
            event.preventDefault()
            first.focus()
        }
    })

    window.addEventListener('resize', positionDetailsPanel)
    window.addEventListener('scroll', () => {
        if (!detailsOverlay.hidden && !mobileDetails.matches) positionDetailsPanel()
    }, { passive: true })
    mobileDetails.addEventListener('change', () => {
        if (detailsOverlay.hidden) return
        detailsOverlay.classList.toggle('is-mobile', mobileDetails.matches)
        positionDetailsPanel()
    })
}

document.querySelectorAll('.add-to-cart-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const artworkId = btn.dataset.artworkId

        fetch(`/cart/add/${artworkId}/`)
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    btn.textContent = 'Added'
                    const counter = document.getElementById('cart-count')
                    if (counter) {
                        counter.textContent = data.cart_count
                        counter.style.display = 'inline-flex'
                    }
                    setTimeout(() => {
                        btn.textContent = 'Add to Cart'
                    }, 1500)
                } else {
                    btn.textContent = 'No more stock'
                    setTimeout(() => {
                        btn.textContent = 'Add to Cart'
                        btn.disabled = false
                    }, 1500)
                }
            })
    })
})
})
