// JoyofCare Main JavaScript
// Handles mobile nav toggle, FAQ accordion, and accessibility improvements

(function() {
  'use strict';

  // Mobile Navigation Toggle
  function initMobileNav() {
    var mobileBtn = document.querySelector('.nav-mobile');
    var navLinks = document.querySelector('.nav-links');

    if (!mobileBtn || !navLinks) return;

    mobileBtn.addEventListener('click', function() {
      var isOpen = navLinks.classList.toggle('nav-open');
      mobileBtn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
      mobileBtn.setAttribute('aria-label', isOpen ? 'Tutup menu' : 'Buka menu');
    });

    // Close mobile menu when clicking outside
    document.addEventListener('click', function(e) {
      if (!navLinks.contains(e.target) && !mobileBtn.contains(e.target) && navLinks.classList.contains('nav-open')) {
        navLinks.classList.remove('nav-open');
        mobileBtn.setAttribute('aria-expanded', 'false');
        mobileBtn.setAttribute('aria-label', 'Buka menu');
      }
    });

    // Close mobile menu on Escape key
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' && navLinks.classList.contains('nav-open')) {
        navLinks.classList.remove('nav-open');
        mobileBtn.setAttribute('aria-expanded', 'false');
        mobileBtn.setAttribute('aria-label', 'Buka menu');
        mobileBtn.focus();
      }
    });
  }

  // FAQ Accordion
  function initFAQ() {
    var faqItems = document.querySelectorAll('.faq-item');
    if (!faqItems.length) return;

    faqItems.forEach(function(item, index) {
      var question = item.querySelector('.faq-question');
      var answer = item.querySelector('.faq-answer');
      if (!question || !answer) return;

      // Set initial ARIA state
      question.setAttribute('aria-expanded', 'false');
      question.setAttribute('aria-controls', 'faq-answer-' + index);
      answer.id = 'faq-answer-' + index;
      answer.setAttribute('role', 'region');

      question.addEventListener('click', function() {
        var isOpen = item.classList.toggle('active');
        question.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
      });
    });
  }

  // Mark current page in nav
  function initActiveNav() {
    var path = window.location.pathname;
    var links = document.querySelectorAll('.nav-links a');
    links.forEach(function(link) {
      var href = link.getAttribute('href');
      if (href && path.indexOf(href) === 0 && href !== '/') {
        link.setAttribute('aria-current', 'page');
      } else if (href === '/' && (path === '/' || path === '/index.html')) {
        link.setAttribute('aria-current', 'page');
      }
    });
  }

  // WhatsApp float button: scroll-aware
  function initWhatsAppFloat() {
    var waFloat = document.querySelector('.wa-float');
    if (!waFloat) return;

    var lastScroll = 0;
    window.addEventListener('scroll', function() {
      var current = window.pageYOffset;
      if (current > 300) {
        waFloat.classList.add('visible');
      } else {
        waFloat.classList.remove('visible');
      }
      lastScroll = current;
    }, { passive: true });
  }

  // Initialize everything when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      initMobileNav();
      initFAQ();
      initActiveNav();
      initWhatsAppFloat();
    });
  } else {
    initMobileNav();
    initFAQ();
    initActiveNav();
    initWhatsAppFloat();
  }
})();
