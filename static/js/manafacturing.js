
const multipleItemCarousel = document.getElementById('testimonialCarousel');
if (multipleItemCarousel && window.innerWidth >= 768) {
  const carousel = new bootstrap.Carousel(multipleItemCarousel, {
    interval: false,
  });

  const carouselInner = document.querySelector('.carousel-inner.testimonial');
  const carouselItem = document.querySelector('.testimonial-item.carousel-item');
  const cardWidth = carouselItem.getBoundingClientRect().width

  let scrollPosition = 0;

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


