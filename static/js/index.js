const items = document.querySelectorAll('.carousel-item.hero');
const nextBtn = document.querySelector('.carousel-control-next.hero');
const prevBtn = document.querySelector('.carousel-control-prev.hero');

let currentIndex = 0;

function showSlide(newIndex) {
  items.forEach((item, idx) => {
    item.classList.remove('active', 'prev-active');
    if (idx === currentIndex) {
      item.classList.add('prev-active');
    }
  });

  items[newIndex].classList.add('active');

  setTimeout(() => {
    items[currentIndex].classList.remove('prev-active');
    currentIndex = newIndex;
  }, 1500); // matches CSS transition duration
}

nextBtn.addEventListener('click', () => {
  const nextIndex = (currentIndex + 1) % items.length;
  showSlide(nextIndex);
});

prevBtn.addEventListener('click', () => {
  const prevIndex = (currentIndex - 1 + items.length) % items.length;
  showSlide(prevIndex);
});

document.addEventListener("DOMContentLoaded", function() {
    const counters = document.querySelectorAll(".counter-number");
    const section = document.querySelector(".brand-section"); // Target section

    let observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                resetCounters(); // Reset counters to 0 before starting again
                startCounter(); // Run counter animation
            }
        });
    }, { threshold: 0.5 }); // Trigger when 50% of the section is visible

    observer.observe(section);

    function resetCounters() {
        counters.forEach(counter => {
            counter.innerText = "0"; // Reset to 0 every time section appears
        });
    }

    function startCounter() {
        counters.forEach(counter => {
            let target = +counter.getAttribute("data-target"); // Fetch target value
            let count = 0;
            let step = Math.ceil(target / 100); // Adjust speed

            function updateCounter() {
                count += step;
                if (count >= target) {
                    counter.innerText = target + "+"; // Stop at final value
                } else {
                    counter.innerText = count;
                    requestAnimationFrame(updateCounter);
                }
            }

            updateCounter(); // Start animation
        });
    }
});

document.addEventListener("DOMContentLoaded", function () {
    // const accordionButtons = document.querySelectorAll(".accordion-button");
    const heroSection = document.getElementById("hero-intro-section");
    setTimeout(() => {
      if (heroSection) {
          heroSection.classList.add("hero-introduction-loader"); // Replace "new-class" with the desired class name
      }
  }, 1400); // 1000ms = 1 second

    // accordionButtons.forEach(button => {
    //     button.addEventListener("click", function () {
    //       event.preventDefault();
    //         const icon = this.querySelector(".icon");
    //         if ( this.classList.contains("collapsed")) {
    //             icon.textContent = "+";
    //         }
    //         else {
    //             icon.textContent = "-";
    //         }
    //         // Toggle between + and -
    //         setTimeout(() => {
    //             if (this.classList.contains("collapsed")) {
    //                 icon.textContent = "+";
    //             } else {
    //                 icon.textContent = "-";
    //             }
    //         }, 100); // Small delay to sync with Bootstrap animation
    //     });
    // });
});



const multipleItemCarousel = document.getElementById('testimonialCarousel');
if (multipleItemCarousel && window.innerWidth >= 768) {
  const carousel = new bootstrap.Carousel(multipleItemCarousel, {
    interval: false,
  });

  const carouselInner = document.querySelector('.carousel-inner.testimonial');
  const carouselItem = document.querySelector('.testimonial-item.carousel-item');
  const cardWidth = carouselItem.getBoundingClientRect().width

  let scrollPosition = 0;

   // Auto-scroll functionality
   const autoScrollInterval = setInterval(() => {
    if (scrollPosition < carouselInner.scrollWidth - carouselInner.clientWidth) {
      scrollPosition += cardWidth;
      carouselInner.scrollTo({ left: scrollPosition, behavior: 'smooth' });
    } else {
      scrollPosition = 0; // Reset to the beginning when reaching the end
      carouselInner.scrollTo({ left: scrollPosition, behavior: 'smooth' });
    }
  }, 2000); // Auto-scroll every 5 seconds

  document.querySelector('.carousel-control-next.testimonial-button').addEventListener('click', () => {
    console.log("next button clicked")
    if (scrollPosition < carouselInner.scrollWidth - carouselInner.clientWidth) {
      scrollPosition += cardWidth;
      carouselInner.scrollTo({ left: scrollPosition, behavior: 'smooth' });
    }
  });

  document.querySelector('.carousel-control-prev.testimonial-button').addEventListener('click', () => {
    console.log("prev button clicked")
    if (scrollPosition > 0) {
      scrollPosition -= cardWidth;
      carouselInner.scrollTo({ left: scrollPosition, behavior: 'smooth' });
    }
  });
} else if (multipleItemCarousel) {
  multipleItemCarousel.classList.add('slide');
}

