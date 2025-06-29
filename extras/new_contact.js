document.addEventListener('DOMContentLoaded', function () {

    const form = document.getElementById('Contact_Us');
    const errorBox = document.getElementById('error_data');
    const loading = document.getElementById('form_process');
    const modal = document.getElementById("center-modal");
    const closeButton = document.querySelector(".btn-close");

    const dropdownBtn = document.getElementById("dropdownMenuButton");
    const dropdownMenu = document.getElementById("dropdownMenu");
    const contactUs = document.getElementById("contact-us");
    // const navbarDropDown = document.getElementsByClassName("nav-dropdown");
    const navbarDropdownMenu = document.getElementById("customDropdownMenu");

  
    // Get CSRF token from cookie
    function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.startsWith(name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }
  
    form.addEventListener('submit', function (e) {
      console.log("submit form clicked")
      e.preventDefault();
  
      const formData = new FormData(form);
      console.log(formData.entries());

      for (let [key, value] of formData.entries()) {
        formData.set(key, value.trim());
      }
      loading.style.visibility = 'visible';
      errorBox.textContent = '';
  
      fetch(form.action, {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
        },
        body: formData,
      })
        .then((res) => res.json())
        .then((data) => {
          loading.style.visibility = 'hidden';
          if (data.status === 1) {
                
            setTimeout(() => {
                form.reset(); // Reset the form fields
                closeModal(); // Close the modal
            }, 1000);
        }
            else {
            errorBox.textContent = data.error || 'An error occurred.';
          }
        })
        .catch(() => {
          loading.style.visibility = 'hidden';
          errorBox.textContent = 'Server error. Please try again later.';
        });
    });


    
      // navbarDropDown.addEventListener("click", function () {
      //     navbarDropdownMenu.classList.toggle("show");
      // });
      // // Close dropdown when clicking outside
      // document.addEventListener("click", function (event) {
      //     if (!navbarDropDown.contains(event.target) && !navbarDropdownMenu.contains(event.target)) {
      //         navbarDropdownMenu.classList.remove("show");
      //     }
      // });       
    
      // Toggle dropdown on button click
      dropdownBtn.addEventListener("click", function () {
        console.log("Dropdown button clicked");
          const isExpanded=dropdownMenu.classList.toggle("show");
          console.log("Dropdown is expanded: ", isExpanded);
          dropdownBtn.setAttribute("aria-expanded", isExpanded); // Set aria-expanded based on the toggle state
        });
    
      // Close dropdown when clicking outside
      document.addEventListener("click", function (event) {
          if (!dropdownBtn.contains(event.target) && !dropdownMenu.contains(event.target)) {
              dropdownMenu.classList.remove("show");
          }
      });
    
      // Prevent dropdown from closing when clicking inside input fields
      document.addEventListener("click", function (event) {
          if (event.target.tagName === "INPUT" && event.target.classList.contains("form-control")) {
              event.stopPropagation();
          }
      });
    
      // Update dropdown button text when an option is selected
      document.querySelectorAll(".dropdown-item").forEach(item => {
          item.addEventListener("click", () => {
              dropdownBtn.querySelector(".dropdown-placeholder").textContent = item.textContent;
              dropdownMenu.classList.remove("show");
              console.log("Item is selected: " + item.textContent);
          });
      });
      
    
      contactUs.addEventListener("click", function () {
        console.log("Contact us button is clicked");
        const modalBackdrop = document.querySelector(".modal-backdrop");
        console.log("Modal backdrop: ", modalBackdrop);
        let backdrop = document.createElement("div");
                    backdrop.className = "modal-backdrop fade show";
                    document.body.appendChild(backdrop);
    
        // Open modal
        modal.style.display = "block";
        modal.classList.add("show");
        // modalBackdrop.classList.add("show");
    
    
        modal.removeAttribute("aria-hidden");
    });
    
  // function to cloase modal
  function closeModal() {
      console.log("Manually closing modal...");
      // Remove modal visibility
      modal.classList.remove("show");
      modal.style.display = "none";
      modal.ariaHidden="true";
      // Remove Bootstrap modal backdrop manually
      const modalBackdrop = document.querySelector(".modal-backdrop");
      if (modalBackdrop) {
          modalBackdrop.remove();
          setTimeout(() => modalBackdrop.remove(), 200); // Remove it after animation
      }
      // Reset body class and styles
      document.body.classList.remove("modal-open");
      document.body.style.removeProperty("padding-right");
  }
  
  closeButton.addEventListener("click", function() { closeModal(); });
});