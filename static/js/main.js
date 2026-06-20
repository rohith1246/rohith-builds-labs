// ── Mobile Nav ─────────────────────────────────────────────────────────────
const navToggle = document.getElementById('nav-toggle');
const navMobile = document.getElementById('nav-mobile');

if (navToggle && navMobile) {
  navToggle.addEventListener('click', () => {
    navMobile.classList.toggle('open');
    const isOpen = navMobile.classList.contains('open');
    navToggle.setAttribute('aria-expanded', isOpen);
  });

  // Close on link click
  navMobile.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      navMobile.classList.remove('open');
    });
  });

  // Close on outside click
  document.addEventListener('click', (e) => {
    if (!navToggle.contains(e.target) && !navMobile.contains(e.target)) {
      navMobile.classList.remove('open');
    }
  });
}

// ── Active Nav Link ─────────────────────────────────────────────────────────
document.querySelectorAll('.nav-links a').forEach(link => {
  if (link.href === window.location.href) {
    link.classList.add('active');
  }
});

// ── Smooth Scroll for "See Our Work" ───────────────────────────────────────
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      e.preventDefault();
      const offset = 80;
      const top = target.getBoundingClientRect().top + window.pageYOffset - offset;
      window.scrollTo({ top, behavior: 'smooth' });
    }
  });
});

// ── Stats Counter Animation ─────────────────────────────────────────────────
function animateCounters() {
  const counters = document.querySelectorAll('[data-count]');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        const target = parseInt(el.dataset.count, 10);
        const suffix = el.dataset.suffix || '';
        const duration = 1200;
        const start = performance.now();

        function update(now) {
          const elapsed = now - start;
          const progress = Math.min(elapsed / duration, 1);
          const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
          const current = Math.round(eased * target);
          el.textContent = current + suffix;
          if (progress < 1) requestAnimationFrame(update);
        }

        requestAnimationFrame(update);
        observer.unobserve(el);
      }
    });
  }, { threshold: 0.5 });

  counters.forEach(el => observer.observe(el));
}

animateCounters();

// ── Navbar scroll shadow ─────────────────────────────────────────────────────
const navbar = document.querySelector('.navbar');
if (navbar) {
  window.addEventListener('scroll', () => {
    if (window.scrollY > 20) {
      navbar.style.boxShadow = '0 1px 20px rgba(0,0,0,0.4)';
    } else {
      navbar.style.boxShadow = 'none';
    }
  }, { passive: true });
}

// ── Flash message auto-dismiss ───────────────────────────────────────────────
const flashes = document.querySelectorAll('.flash');
flashes.forEach(flash => {
  setTimeout(() => {
    flash.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    flash.style.opacity = '0';
    flash.style.transform = 'translateY(-8px)';
    setTimeout(() => flash.remove(), 500);
  }, 5000);
});

// ── Form submit feedback ─────────────────────────────────────────────────────
const contactForm = document.getElementById('contact-form');
const submitBtn = document.getElementById('submit-btn');

if (contactForm && submitBtn) {
  contactForm.addEventListener('submit', () => {
    submitBtn.textContent = 'Sending...';
    submitBtn.disabled = true;
    submitBtn.style.opacity = '0.7';
  });
}


