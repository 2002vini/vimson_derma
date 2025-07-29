document.addEventListener('DOMContentLoaded', function () {
 
const multipleItemCarousel = document.getElementById('testimonialCarousel');
if (multipleItemCarousel && window.innerWidth >= 768) {
  const carousel = new bootstrap.Carousel(multipleItemCarousel, {
    interval: false,
  });

  const carouselInner = document.querySelector('.carousel-inner.testimonial');
  const carouselItem = document.querySelector('.testimonial-item.carousel-item');
  const cardWidth = carouselItem.getBoundingClientRect().width

  let scrollPosition = 0;
  const scrollStep = 1;
  const scrollDelay=20;
      // Auto-scroll function
    // function autoScroll() {
    //   if (carouselInner.scrollLeft < carouselInner.scrollWidth - carouselInner.clientWidth) {
    //     carouselInner.scrollLeft += scrollStep;
    //   } else {
    //     carouselInner.scrollLeft = 0; // Loop back to start
    //   }
    //   setTimeout(autoScroll, scrollDelay);
    // }
    // autoScroll();

  document.querySelector('.carousel-control-next.testimonial-button').addEventListener('click', () => {
    if (scrollPosition < carouselInner.scrollWidth - carouselInner.clientWidth) {
      scrollPosition += cardWidth;
      carouselInner.scrollTo({ left: scrollPosition, behavior: 'smooth' });
    }
  });

  document.querySelector('.carousel-control-prev.testimonial-button').addEventListener('click', () => {
    if (scrollPosition > 0) {
      scrollPosition -= cardWidth;
      carouselInner.scrollTo({ left: scrollPosition, behavior: 'smooth' });
    }
  });
} else if (multipleItemCarousel) {
  multipleItemCarousel.classList.add('slide');
}

    const accordionButtons = document.querySelectorAll(".accordion-button");

    accordionButtons.forEach(button => {
      button.addEventListener("click", function () {
        const icon = this.querySelector(".icon");
        // Toggle between + and -
        setTimeout(() => {
          if (this.classList.contains("collapsed")) {
            console.log("Collapsed");
            icon.textContent = "+";
          } else {
            console.log("Expanded");
            icon.textContent = "-";
          }
        }, 100); // Small delay to sync with Bootstrap animation
      });
    });
 

  const steps = document.querySelectorAll(".step");

  steps.forEach(step => {
    step.addEventListener("click", () => {
      step.classList.toggle("active"); // Toggles the 'active' class
    });
  });
});

