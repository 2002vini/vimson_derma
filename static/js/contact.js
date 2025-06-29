document.addEventListener('DOMContentLoaded', function () {

    const form = document.getElementById('Contact_Us');
    const request_quote= document.getElementById('Request_Quote');
    const form_banner = document.getElementById('Contact_Us_banner');

  
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

    document.getElementById("closeModalButton").addEventListener("click", function () {
        errorBox.textContent = '';
        errorBox.style.color = 'red';
    });
    document.getElementById("closeModalButtonRequest").addEventListener("click", function () {
        errorBox.textContent = '';
        errorBox.style.color = 'red';
    });
    function submitForm(form,formData,errorBox,loading){
        console.log("form action is:",form.action);
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
              const originalFormHTML = form.innerHTML; // Store the original form HTML
              if (data.status === 1) {
                    
                    form.reset(); // Reset the form fields
                    errorBox.textContent = 'Your message has been sent successfully.';
                    errorBox.style.color = 'green'; // Change text color to green
                    errorBox.style.fontWeight = 'bold'; // Make text bold
                    errorBox.style.fontSize = '16px'; // Increase font size
            }
                else {
                errorBox.style.color = 'red'; // Change text color to red
                errorBox.style.fontWeight = 'bold'; // Make text bold
                errorBox.style.fontSize = '16px'; // Increase font size
                errorBox.textContent = data.error || 'An error occurred.';
              }
            })
            .catch(() => {
              loading.style.visibility = 'hidden';
              errorBox.textContent = 'Server error. Please try again later.';
            });
    }
    form.addEventListener('submit', function (e) {
      console.log("submit form clicked")
      e.preventDefault();
      const errorBox = document.getElementById('error_data');
      const loading = document.getElementById('form_process');
        console.log("error box is:",errorBox);
        console.log("loading is:",loading);
      const formData = new FormData(form);
      submitForm(form,formData,errorBox,loading);
    });

    request_quote.addEventListener('submit', function (e) {
        e.preventDefault();
        console.log("request quote clicked")
        const errorBox = document.getElementById('error_data_request');
        const loading = document.getElementById('form_process_request');
        const formData = new FormData(request_quote);
        submitForm(request_quote,formData,errorBox,loading);
    }
    );

    form_banner.addEventListener('submit', function (e) {
        e.preventDefault();
        console.log("form banner clicked")
        const errorBox = document.getElementById('error_data_banner');
        const loading = document.getElementById('form_process_banner');
        const formData = new FormData(form_banner);
        submitForm(form_banner,formData,errorBox,loading);
    });

    const dropdownButton = document.getElementById('dropdownMenuButton');
        const dropdownItems = document.querySelectorAll('.modal-item');
    
        dropdownItems.forEach(item => {
            item.addEventListener('click', function (e) {
                e.preventDefault(); // Prevent default link behavior
                const selectedText = this.textContent; // Get the text of the clicked item
                console.log(selectedText);
                console.log("previous selected text was:", dropdownButton.innerText);
                dropdownButton.innerText = selectedText; // Update the button text
            });
        });
    
    const dropdownButtonRequest = document.getElementById('dropdownMenuButtonRequest');
        const dropdownItemsRequest = document.querySelectorAll('.dropdown-item-request');
    
        dropdownItemsRequest.forEach(item => {
            item.addEventListener('click', function (e) {
                e.preventDefault(); // Prevent default link behavior
                const selectedText = this.textContent; // Get the text of the clicked item
                console.log(selectedText);
                console.log("previous selected text was:", dropdownButtonRequest.innerText);
                dropdownButtonRequest.innerText = selectedText; // Update the button text
            });
        });

})