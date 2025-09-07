document.addEventListener('DOMContentLoaded', function () {

document.querySelectorAll(".category-item").forEach(item => {
    item.addEventListener("click", function () {
        const value = this.getAttribute("data-value");

        // update button text
        document.getElementById("categoryDropdownButton").textContent = value;

        // store value in hidden input for form submission
        document.getElementById("category").value = value;
    });
});



    const dropdownButton = document.getElementById('dropdownMenuButton');
        const dropdownItems = document.querySelectorAll('.modal-item');
    
        dropdownItems.forEach(item => {
            item.addEventListener('click', function (e) {
                e.preventDefault(); // Prevent default link behavior
                const selectedText = this.textContent; // Get the text of the clicked item
                dropdownButton.innerText = selectedText; // Update the button text
            });
        });
    
    const dropdownButtonRequest = document.getElementById('dropdownMenuButtonRequest');
        const dropdownItemsRequest = document.querySelectorAll('.dropdown-item-request');
    
        dropdownItemsRequest.forEach(item => {
            item.addEventListener('click', function (e) {
                e.preventDefault(); // Prevent default link behavior
                const selectedText = this.textContent; // Get the text of the clicked item
                dropdownButtonRequest.innerText = selectedText; // Update the button text
            });
        });

})

