/* ==========================================================================
   Estellar Jewelry Premium Interactivity Engine
   Designed for: Alex (ChoiGPT Corp.)
   Includes: Smooth Scroll, Intersection Observers, Custom Filtering & Booking
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  initNavigation();
  initScrollAnimations();
  initProductFilter();
  initBookingForm();
  initYouTubeTriggers();
});

/**
 * 1. Mobile Navigation & Header Scroll State
 */
function initNavigation() {
  const header = document.getElementById('main-header');
  const navMenu = document.getElementById('nav-menu');
  const navToggle = document.getElementById('nav-toggle');
  const navLinks = document.querySelectorAll('.nav-link');

  // Toggle mobile menu
  if (navToggle && navMenu) {
    navToggle.addEventListener('click', () => {
      navMenu.classList.toggle('active');
      const icon = navToggle.querySelector('i');
      if (icon) {
        if (navMenu.classList.contains('active')) {
          icon.className = 'fa-solid fa-xmark';
        } else {
          icon.className = 'fa-solid fa-bars';
        }
      }
    });
  }

  // Close mobile menu when a link is clicked
  navLinks.forEach(link => {
    link.addEventListener('click', () => {
      if (navMenu) {
        navMenu.classList.remove('active');
      }
      const icon = navToggle ? navToggle.querySelector('i') : null;
      if (icon) {
        icon.className = 'fa-solid fa-bars';
      }
    });
  });

  // Add scroll class to header
  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  });
}

/**
 * 2. High-Performance Scroll Reveal (using Intersection Observer)
 */
function initScrollAnimations() {
  const reveals = document.querySelectorAll('.reveal');
  
  const revealOptions = {
    threshold: 0.15,
    rootMargin: '0px 0px -50px 0px'
  };

  const revealObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('active');
        // Once revealed, no need to keep observing
        observer.unobserve(entry.target);
      }
    });
  }, revealOptions);

  reveals.forEach(reveal => {
    revealObserver.observe(reveal);
  });
}

/**
 * 3. Masterpiece Category Filtering
 */
function initProductFilter() {
  const filterButtons = document.querySelectorAll('.filter-btn');
  const prdCards = document.querySelectorAll('.prd-card');
  const grid = document.getElementById('collection-grid');

  filterButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      // Remove active class from all buttons
      filterButtons.forEach(button => button.classList.remove('active'));
      // Add active class to clicked button
      btn.classList.add('active');

      const filterValue = btn.getAttribute('data-filter');

      // Grid visual feedback during reload
      if (grid) {
        grid.style.opacity = '0.3';
        grid.style.transform = 'translateY(10px)';
        grid.style.transition = 'all 0.3s ease';
      }

      setTimeout(() => {
        prdCards.forEach(card => {
          const category = card.getAttribute('data-category');
          
          if (filterValue === 'all' || category === filterValue) {
            card.style.display = 'block';
            // Subtle pop animation
            card.style.animation = 'fadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards';
          } else {
            card.style.display = 'none';
          }
        });

        if (grid) {
          grid.style.opacity = '1';
          grid.style.transform = 'translateY(0)';
        }
      }, 300);
    });
  });
}

/**
 * 4. Interactive Consultation Request Simulation
 */
function initBookingForm() {
  const form = document.getElementById('showroom-form');
  
  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();

      const name = document.getElementById('booking-name').value;
      const phone = document.getElementById('booking-phone').value;
      const type = document.getElementById('booking-type');
      const typeText = type.options[type.selectedIndex].text;
      const date = document.getElementById('booking-date').value;

      // Formatting ISO DateTime to human readable Korean Format
      let formattedDate = date;
      try {
        const d = new Date(date);
        formattedDate = `${d.getFullYear()}년 ${d.getMonth() + 1}월 ${d.getDate()}일 ${d.getHours()}시 ${d.getMinutes()}분`;
      } catch (err) {
        console.error("Date formatting failed", err);
      }

      // Elegant Custom Feedback Modal (using browser alert as fallback, styled console logging)
      const message = `✨ [ESTELLAR Showroom Reservation Request] ✨\n\n조예은 디렉터와의 1:1 프라이빗 상담 신청이 완료되었습니다.\n\n• 예약자명: ${name} 님\n• 연락처: ${phone}\n• 상담 분야: ${typeText}\n• 희망 시간: ${formattedDate}\n\n신청 내용 검토 후 보석 감정사 디렉터가 2시간 이내에 직접 안내 전화를 드리겠습니다. 감사합니다.`;
      
      alert(message);

      // Reset form
      form.reset();

      // Proactively guide user to Naver Map Place to solidify booking if they want instant confirmation
      const confirmNaver = confirm("네이버 예약을 통해 실시간으로 확정 예약을 진행하시겠습니까?");
      if (confirmNaver) {
        window.open('https://map.naver.com/p/entry/place/1184031939', '_blank');
      }
    });
  }
}

/**
 * 5. YouTube Video Trigger
 */
function initYouTubeTriggers() {
  const trigger = document.getElementById('yt-video-trigger');
  
  if (trigger) {
    trigger.addEventListener('click', () => {
      // Elegant navigation to Youtube Chanel inside a new window
      window.open('https://www.youtube.com/@%EC%A1%B0%EC%98%88%EC%9D%80-x6y', '_blank');
    });
  }
}
