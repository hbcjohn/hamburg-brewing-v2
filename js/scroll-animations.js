/**
 * Scroll Animations Engine for Hamburg Brewing v3
 * Handles IntersectionObserver-based reveal animations,
 * scroll progress bar, and scroll-driven effects.
 */

(function() {
  'use strict';

  // ── 1. Scroll Progress Bar (JS fallback for browsers without scroll-timeline) ──
  const progressBar = document.querySelector('.scroll-progress-bar');

  function updateScrollProgress() {
    if (!progressBar) return;
    const scrollTop = window.scrollY || document.documentElement.scrollTop;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
    progressBar.style.width = progress + '%';
  }

  window.addEventListener('scroll', updateScrollProgress, { passive: true });
  updateScrollProgress();


  // ── 2. IntersectionObserver Reveal System ──
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('revealed');
        // Optionally stop observing after first reveal
        // revealObserver.unobserve(entry.target);
      }
    });
  }, {
    root: null,
    rootMargin: '0px 0px -60px 0px',
    threshold: 0.1
  });

  function initRevealAnimations() {
    const reveals = document.querySelectorAll(
      '.reveal, .reveal-left, .reveal-right, .reveal-up, .reveal-scale, .stagger-children'
    );
    reveals.forEach(el => revealObserver.observe(el));
  }

  // Also handle section-divider animated elements
  const dividerObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('revealed');
        dividerObserver.unobserve(entry.target);
      }
    });
  }, {
    root: null,
    rootMargin: '0px',
    threshold: 0.5
  });

  function initDividerAnimations() {
    const dividers = document.querySelectorAll('.section-divider.animated');
    dividers.forEach(el => dividerObserver.observe(el));
  }


  // ── 3. Parallax via JS (fallback for browsers without scroll-timeline) ──
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const supportsScrollTimeline = CSS.supports('animation-timeline', 'scroll()');

  function initParallax() {
    if (prefersReducedMotion || supportsScrollTimeline) return;

    const heroBg = document.querySelector('.hero-bg');
    if (!heroBg) return;

    let ticking = false;
    window.addEventListener('scroll', () => {
      if (!ticking) {
        requestAnimationFrame(() => {
          const scrollY = window.scrollY;
          const maxScroll = window.innerHeight * 0.8;
          const progress = Math.min(scrollY / maxScroll, 1);
          const translateY = -10 + (progress * 20); // -10% to +10%
          const scale = 1.1 - (progress * 0.1);     // 1.1 to 1.0
          heroBg.style.transform = `translateY(${translateY}%) scale(${scale})`;
          ticking = false;
        });
        ticking = true;
      }
    }, { passive: true });
  }


  // ── 4. Hero Content Fade on Scroll ──
  function initHeroFade() {
    if (prefersReducedMotion || supportsScrollTimeline) return;

    const heroContent = document.querySelector('.hero-content');
    if (!heroContent) return;

    let ticking = false;
    window.addEventListener('scroll', () => {
      if (!ticking) {
        requestAnimationFrame(() => {
          const scrollY = window.scrollY;
          const maxScroll = window.innerHeight * 0.6;
          const progress = Math.min(scrollY / maxScroll, 1);
          const opacity = 1 - progress;
          const translateY = -progress * 60;
          const scale = 1 - (progress * 0.08);
          heroContent.style.opacity = opacity;
          heroContent.style.transform = `translateY(${translateY}px) scale(${scale})`;
          ticking = false;
        });
        ticking = true;
      }
    }, { passive: true });
  }


  // ── 5. Parallax Image Sections ──
  function initParallaxImages() {
    if (prefersReducedMotion || supportsScrollTimeline) return;

    const parallaxImages = document.querySelectorAll('.parallax-image img');
    if (!parallaxImages.length) return;

    const imageObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        const img = entry.target;
        if (entry.isIntersecting) {
          img.dataset.parallaxActive = 'true';
        } else {
          img.dataset.parallaxActive = 'false';
        }
      });
    }, { threshold: 0 });

    parallaxImages.forEach(img => imageObserver.observe(img));

    let ticking = false;
    window.addEventListener('scroll', () => {
      if (!ticking) {
        requestAnimationFrame(() => {
          parallaxImages.forEach(img => {
            if (img.dataset.parallaxActive !== 'true') return;
            const rect = img.getBoundingClientRect();
            const windowHeight = window.innerHeight;
            const progress = (windowHeight - rect.top) / (windowHeight + rect.height);
            const clamped = Math.max(0, Math.min(1, progress));
            const translateY = -40 + (clamped * 80); // -40px to +40px
            const scale = 1.08 - (Math.abs(clamped - 0.5) * 0.06); // subtle scale
            img.style.transform = `translateY(${translateY}px) scale(${scale})`;
          });
          ticking = false;
        });
        ticking = true;
      }
    }, { passive: true });
  }


  // ── 6. Header shrink on scroll ──
  function initHeaderShrink() {
    const header = document.querySelector('.site-header');
    if (!header) return;

    let lastScroll = 0;
    window.addEventListener('scroll', () => {
      const scrollY = window.scrollY;
      if (scrollY > 100) {
        header.classList.add('scrolled');
      } else {
        header.classList.remove('scrolled');
      }
      lastScroll = scrollY;
    }, { passive: true });
  }


  // ── 7. Morph cards subtle tilt on mouse move (desktop only) ──
  function initMorphCards() {
    if (window.matchMedia('(pointer: coarse)').matches) return;

    const cards = document.querySelectorAll('.morph-card');
    cards.forEach(card => {
      card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        const rotateX = (y - centerY) / centerY * -4;
        const rotateY = (x - centerX) / centerX * 4;
        card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-8px) scale(1.02)`;
      });

      card.addEventListener('mouseleave', () => {
        card.style.transform = '';
      });
    });
  }


  // ── Initialize everything on DOM ready ──
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      initRevealAnimations();
      initDividerAnimations();
      initParallax();
      initHeroFade();
      initParallaxImages();
      initHeaderShrink();
      initMorphCards();
    });
  } else {
    initRevealAnimations();
    initDividerAnimations();
    initParallax();
    initHeroFade();
    initParallaxImages();
    initHeaderShrink();
    initMorphCards();
  }

})();
