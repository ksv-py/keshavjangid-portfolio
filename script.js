// Keshav Jangid — Portfolio v2 | Vanilla JS micro-animations
(function () {
  "use strict";

  // Footer year
  var yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  // Sticky nav: shrink + shadow on scroll
  var nav = document.getElementById("nav");
  function onScroll() {
    if (nav) nav.classList.toggle("scrolled", window.scrollY > 24);
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  // Mobile nav toggle (hamburger)
  var toggle = document.getElementById("navToggle");
  var links = document.getElementById("navLinks");
  if (toggle && links) {
    toggle.addEventListener("click", function () {
      var open = links.classList.toggle("open");
      toggle.classList.toggle("open", open);
      toggle.setAttribute("aria-expanded", String(open));
    });
    links.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () {
        links.classList.remove("open");
        toggle.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  // Reveal on scroll (IntersectionObserver)
  var revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var revealObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          revealObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    revealEls.forEach(function (el) { revealObserver.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("visible"); });
  }

  // Animated skill bars: fill when visible
  var fills = document.querySelectorAll(".bar .fill");
  if ("IntersectionObserver" in window) {
    var barObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.style.width = entry.target.getAttribute("data-width") || "70%";
          barObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });
    fills.forEach(function (f) { barObserver.observe(f); });
  } else {
    fills.forEach(function (f) { f.style.width = f.getAttribute("data-width") || "70%"; });
  }

  // Hero typing effect
  var typedEl = document.getElementById("typed");
  var phrases = [
    "Backend & ML Engineer",
    "Python · Flask / FastAPI · React",
    "ML & Data Enthusiast",
    "Building things that ship"
  ];
  if (typedEl) {
    var phraseIndex = 0, charIndex = 0, deleting = false;
    (function type() {
      var current = phrases[phraseIndex];
      if (deleting) {
        charIndex -= 1;
        typedEl.textContent = current.slice(0, charIndex);
        if (charIndex === 0) {
          deleting = false;
          phraseIndex = (phraseIndex + 1) % phrases.length;
          setTimeout(type, 350);
          return;
        }
        setTimeout(type, 28);
      } else {
        charIndex += 1;
        typedEl.textContent = current.slice(0, charIndex);
        if (charIndex === current.length) {
          deleting = true;
          setTimeout(type, 2000);
          return;
        }
        setTimeout(type, 55);
      }
    })();
  }

  // Project filters: All / Live / Code
  var filterBtns = document.querySelectorAll(".filter-btn");
  var cards = document.querySelectorAll(".project-card");
  filterBtns.forEach(function (btn) {
    btn.addEventListener("click", function () {
      filterBtns.forEach(function (b) { b.classList.remove("active"); });
      btn.classList.add("active");
      var filter = btn.getAttribute("data-filter");
      cards.forEach(function (card) {
        var show = filter === "all" || card.getAttribute("data-type") === filter;
        card.classList.toggle("hidden-card", !show);
        if (show) {
          card.classList.add("visible");
          card.style.animation = "none";
          void card.offsetWidth; // restart pop-in
          card.style.animation = "";
        }
      });
    });
  });

  // Button ripple effect
  document.querySelectorAll(".btn").forEach(function (btn) {
    btn.addEventListener("click", function (e) {
      var rect = btn.getBoundingClientRect();
      var ripple = document.createElement("span");
      ripple.className = "ripple";
      var size = Math.max(rect.width, rect.height);
      ripple.style.width = ripple.style.height = size + "px";
      ripple.style.left = (e.clientX - rect.left - size / 2) + "px";
      ripple.style.top = (e.clientY - rect.top - size / 2) + "px";
      btn.appendChild(ripple);
      setTimeout(function () { ripple.remove(); }, 650);
    });
  });
})();
