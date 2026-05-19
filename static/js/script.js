// ===== DOM Elements (with null guards) =====
const scrollProgressEl = document.getElementById('scrollProgress');
const header = document.getElementById('header');
const navToggle = document.getElementById('navToggle');
const navMenu = document.getElementById('navMenu');
const sections = document.querySelectorAll('section');
const navLinks = document.querySelectorAll('.nav-link');

// ===== Single Scroll Listener (optimized with rAF) =====
let ticking = false;

window.addEventListener('scroll', () => {
  if (!ticking) {
    window.requestAnimationFrame(() => {
      handleScroll();
      ticking = false;
    });
    ticking = true;
  }
});

function handleScroll() {
  const scrollTop = window.scrollY;
  const scrollHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;

  // Scroll Progress Bar
  if (scrollProgressEl && scrollHeight > 0) {
    const progress = (scrollTop / scrollHeight) * 100;
    scrollProgressEl.style.width = progress + '%';
  }

  // Header Sticky Effect
  if (header) {
    if (scrollTop > 50) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  }

  // Active Navigation Link
  let current = '';
  sections.forEach(section => {
    const sectionTop = section.offsetTop;
    if (scrollTop >= sectionTop - 200) {
      current = section.getAttribute('id');
    }
  });

  navLinks.forEach(link => {
    link.classList.remove('active');
    if (link.getAttribute('href') === '#' + current) {
      link.classList.add('active');
    }
  });
}

// ===== Scroll Reveal Animation =====
const observerOptions = {
  threshold: 0.1,
  rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
    }
  });
}, observerOptions);

sections.forEach(section => {
  if (!section.classList.contains('visible')) {
    observer.observe(section);
  }
});

// ===== Mobile Hamburger Menu =====
if (navToggle && navMenu) {
  const overlay = document.createElement('div');
  overlay.classList.add('nav-overlay');
  document.body.appendChild(overlay);

  function openMenu() {
    navToggle.classList.add('active');
    navMenu.classList.add('open');
    overlay.classList.add('active');
    navToggle.setAttribute('aria-expanded', 'true');
    navToggle.setAttribute('aria-label', 'Fermer le menu');
    document.body.style.overflow = 'hidden';
  }

  function closeMenu() {
    navToggle.classList.remove('active');
    navMenu.classList.remove('open');
    overlay.classList.remove('active');
    navToggle.setAttribute('aria-expanded', 'false');
    navToggle.setAttribute('aria-label', 'Ouvrir le menu');
    document.body.style.overflow = '';
  }

  navToggle.addEventListener('click', () => {
    if (navMenu.classList.contains('open')) {
      closeMenu();
    } else {
      openMenu();
    }
  });

  overlay.addEventListener('click', closeMenu);

  navLinks.forEach(link => {
    link.addEventListener('click', closeMenu);
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && navMenu.classList.contains('open')) {
      closeMenu();
    }
  });

  window.addEventListener('resize', () => {
    if (window.innerWidth > 768 && navMenu.classList.contains('open')) {
      closeMenu();
    }
  });
}

// ===== Theme Toggle (Dark/Light Mode) =====
const themeToggle = document.getElementById('themeToggle');
const themeIcon = document.getElementById('themeIcon');

if (themeToggle && themeIcon) {
  // Check local storage for preference
  const currentTheme = localStorage.getItem('portfolioTheme') || 'dark';
  
  if (currentTheme === 'light') {
    document.documentElement.setAttribute('data-theme', 'light');
    themeIcon.classList.remove('ri-moon-line');
    themeIcon.classList.add('ri-sun-line');
  }

  themeToggle.addEventListener('click', () => {
    let theme = document.documentElement.getAttribute('data-theme');
    
    if (theme === 'light') {
      document.documentElement.removeAttribute('data-theme');
      localStorage.setItem('portfolioTheme', 'dark');
      themeIcon.classList.remove('ri-sun-line');
      themeIcon.classList.add('ri-moon-line');
    } else {
      document.documentElement.setAttribute('data-theme', 'light');
      localStorage.setItem('portfolioTheme', 'light');
      themeIcon.classList.remove('ri-moon-line');
      themeIcon.classList.add('ri-sun-line');
    }
  });
}