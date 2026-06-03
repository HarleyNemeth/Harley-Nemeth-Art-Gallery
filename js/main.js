gsap.registerPlugin(ScrollTrigger)

document.addEventListener('DOMContentLoaded', () => {

    const banner = document.querySelector('.banner-container')
    if (banner) {
        const bannerHeight = banner.offsetHeight
        const imgHeight = 160
        const total = bannerHeight + imgHeight * 2

        const leftPositions = [5, 18, 30, 42, 54, 66, 78, 88]

document.querySelectorAll('.float-img').forEach((img, i) => {
    const duration = 7 + Math.random() * 8
    const opacity = 0.5 + Math.random() * 0.5
    const startY = -(imgHeight + Math.random() * bannerHeight)

    gsap.set(img, {
        opacity: opacity,
        left: `${leftPositions[i % leftPositions.length]}%`,
        y: startY
    })

    gsap.to(img, {
    y: `+=${total}`,
    duration: duration,
    ease: "none",
    repeat: -1,
    modifiers: {
        y: gsap.utils.unitize(y => {
            let val = parseFloat(y) % total
            if (val < -imgHeight) val += total
            return val
        })
    }
})
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

})