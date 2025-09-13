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

document.getElementById("request-product").addEventListener("change", function() {
    let categoryId = this.value;
    console.log("Selected category ID:", categoryId);
    if (categoryId) {
        fetch(`/get-subcategories/${categoryId}/`)
            .then(res => res.json())
            .then(data => {
                let subcatSelect = document.getElementById("subcategory");
                subcatSelect.innerHTML = "<option value=''>Select SubCategory</option>";
                data.forEach(item => {
                    console.log("fetced subcategories!");
                    console.log(item.type);
                    subcatSelect.innerHTML += `<option value="${item.id}">${item.type}</option>`;
                });
                document.getElementById("product").innerHTML = "<option value=''>Select Product</option>";
                subcatSelect.disabled = false;
                let prodSelect = document.getElementById("product");
                prodSelect.innerHTML = "<option value='' disabled selected>Select product</option>";
                prodSelect.disabled = true;
            });
        
       
    }
});

document.getElementById("subcategory").addEventListener("change", function() {
    let subcatId = this.value;
    let categoryId = document.getElementById("request-product").value;

    if (subcatId) {
        fetch(`/get-products/?category_id=${categoryId}&subcategory_id=${subcatId}`)
            .then(res => res.json())
            .then(data => {
                let prodSelect = document.getElementById("product");
                prodSelect.innerHTML = "<option value=''>Select Product</option>";
                data.products.forEach(item => {
                    prodSelect.innerHTML += `<option value="${item.id}">${item.name}</option>`;
                });
            prodSelect.disabled = false;

            });

    }
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

