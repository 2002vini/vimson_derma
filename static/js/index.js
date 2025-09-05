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

    const accordionButtons = document.querySelectorAll(".accordion-button");


    accordionButtons.forEach(button => {
        button.addEventListener("click", function () {
          event.preventDefault();
            const icon = this.querySelector(".icon");
            if ( this.classList.contains("collapsed")) {
                icon.textContent = "+";
            }
            else {
                icon.textContent = "-";
            }
            // Toggle between + and -
            setTimeout(() => {
                if (this.classList.contains("collapsed")) {
                    icon.textContent = "+";
                } else {
                    icon.textContent = "-";
                }
            }, 100); // Small delay to sync with Bootstrap animation
        });
    });
});



