document.addEventListener("DOMContentLoaded", function() {

  // Бургер-меню
  (function(){
    const openBtn = document.getElementById('mobileMenuBtn');
    const fullMenu = document.getElementById('mobileFullMenu');
    const mobileNav = document.getElementById('mobileMenuNav');
    const sourceNav = document.querySelector('.carousel-overlay .nav-links');

    if(openBtn && fullMenu && sourceNav){
      mobileNav.innerHTML = sourceNav.innerHTML;
      const pageCarousel = document.querySelector('#carouselExampleControls');

      function toggleMenu(e) {
        e.stopPropagation();
        e.preventDefault();
        e.stopImmediatePropagation();
        const isOpen = fullMenu.classList.contains('active');
        isOpen ? closeMenu() : openMenu();
      }

      function openMenu() {
        fullMenu.style.display = 'flex';
        fullMenu.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden';
        setTimeout(() => {
          fullMenu.classList.add('active');
          openBtn.classList.add('active');
        }, 10);
        if(pageCarousel) pageCarousel.style.pointerEvents = 'none';
      }

      function closeMenu(e) {
        if(e) {
          e.stopPropagation();
          e.preventDefault();
        }
        fullMenu.classList.remove('active');
        openBtn.classList.remove('active');
        setTimeout(() => {
          fullMenu.style.display = 'none';
          fullMenu.setAttribute('aria-hidden', 'true');
          document.body.style.overflow = '';
        }, 400);
        if(pageCarousel) pageCarousel.style.pointerEvents = '';
      }

      openBtn.addEventListener('click', toggleMenu, {capture: true});
      openBtn.addEventListener('touchstart', toggleMenu, {passive: false, capture: true});
      openBtn.addEventListener('touchend', function(e){
        e.preventDefault();
        e.stopPropagation();
        e.stopImmediatePropagation();
      }, {passive: false, capture: true});

      mobileNav.addEventListener('click', (e) => {
        if(e.target.tagName === 'A') closeMenu();
      });

      fullMenu.addEventListener('click', (e) => {
        if(e.target === fullMenu) closeMenu();
      });

      document.addEventListener('keydown', (e) => {
        if(e.key === 'Escape' && fullMenu.classList.contains('active')) closeMenu();
      });
    }
  })();

  // Lightbox для изображений
  (function(){
    const items = document.querySelectorAll('.image-item img');
    const lightbox = document.getElementById('imageLightbox');
    const lbImg = document.getElementById('lightboxImg');
    const close = document.getElementById('lightboxClose');
    const next = document.getElementById('lightboxNext');
    const prev = document.getElementById('lightboxPrev');
    let currentIndex = -1;
    const srcs = Array.from(items).map(i => i.src);

    function open(index) {
      currentIndex = index;
      lbImg.src = srcs[currentIndex];
      lightbox.style.display = 'flex';
      lightbox.setAttribute('aria-hidden','false');
      document.body.style.overflow = 'hidden';
    }

    function closeLB() {
      lightbox.style.display = 'none';
      lightbox.setAttribute('aria-hidden','true');
      document.body.style.overflow = '';
    }

    function nextImg() { if(currentIndex < srcs.length - 1) open(currentIndex + 1); }
    function prevImg() { if(currentIndex > 0) open(currentIndex - 1); }

    items.forEach((img, idx) => img.addEventListener('click', () => open(idx)));
    if(close) close.addEventListener('click', closeLB);
    if(next) next.addEventListener('click', nextImg);
    if(prev) prev.addEventListener('click', prevImg);
    lightbox.addEventListener('click', (e) => { if(e.target === lightbox) closeLB(); });
    document.addEventListener('keydown', (e) => {
      if(e.key === 'Escape') closeLB();
      if(e.key === 'ArrowRight') nextImg();
      if(e.key === 'ArrowLeft') prevImg();
    });
  })();

  // Карусель свайпы
  (function(){
    const carouselEl = document.querySelector('#carouselExampleControls');
    if (carouselEl) {
      let touchStartX = null;
      carouselEl.addEventListener('touchstart', function(e){
        if(!e.target.closest('.mobile-menu-button')){
          touchStartX = e.changedTouches[0].clientX;
        }
      }, {passive:true});

      carouselEl.addEventListener('touchend', function(e){
        if(touchStartX === null) return;
        if(e.target.closest('.mobile-menu-button')) return;
        const diff = touchStartX - e.changedTouches[0].clientX;
        if(Math.abs(diff) > 40){
          const bsCarousel = bootstrap.Carousel.getInstance(carouselEl) || new bootstrap.Carousel(carouselEl);
          if (diff > 0) bsCarousel.next(); else bsCarousel.prev();
        }
        touchStartX = null;
      });

      const prevBtn = carouselEl.querySelector('.carousel-control-prev');
      const nextBtn = carouselEl.querySelector('.carousel-control-next');
      if(prevBtn) prevBtn.style.zIndex = 1050;
      if(nextBtn) nextBtn.style.zIndex = 1050;
    }
  })();

  // Аккордеон aria
  const accordionItems = document.querySelectorAll('#faqAccordion .accordion-item');
  accordionItems.forEach(item => {
    const btn = item.querySelector('.accordion-button');
    const collapse = item.querySelector('.accordion-collapse');
    if (!btn || !collapse) return;
    btn.setAttribute('aria-expanded', collapse.classList.contains('show') ? 'true' : 'false');
    collapse.addEventListener('shown.bs.collapse', () => btn.setAttribute('aria-expanded','true'));
    collapse.addEventListener('hidden.bs.collapse', () => btn.setAttribute('aria-expanded','false'));
  });
});