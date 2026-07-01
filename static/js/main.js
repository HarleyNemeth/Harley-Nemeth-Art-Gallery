gsap.registerPlugin(ScrollTrigger)

document.addEventListener('DOMContentLoaded', () => {

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
    })
})

javascriptdocument.querySelectorAll('.add-to-cart-btn').forEach(btn => {
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