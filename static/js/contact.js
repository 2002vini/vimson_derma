document.addEventListener('DOMContentLoaded', function () {
    const productRange = document.getElementById("product-range");
    const category = document.getElementById("request-product");
    const subcategory = document.getElementById("subcategory");
    const product = document.getElementById("product");

     function resetDropdowns() {
        category.disabled = true;
        category.value = "";
        subcategory.disabled = true;
        subcategory.innerHTML = `<option value="" disabled selected>Select sub category</option>`;
        product.disabled = true;
        product.innerHTML = `<option value="" disabled selected>Select product</option>`;
    }

    resetDropdowns(); // initial reset


    // Step 1: Product Range selected → enable Category
    productRange.addEventListener("change", function() {
        resetDropdowns();
        category.disabled = false;
    });

    category.addEventListener("change", function() {
    const range = productRange.value;
    const catId = category.value;
    console.log("Selected Range:", range);
    console.log("Selected Category ID:", catId);

    product.disabled = true;
    product.innerHTML = `<option value="" disabled selected>Select product</option>`;

    if (range === "Dermatology") {
        console.log("Fetching products for Dermatology");
        subcategory.innerHTML = `<option value="" disabled selected disabled>Select sub category</option>`;
        // Direct fetch products with category + range
        fetch(`/products/?category=${catId}&range=Medicated`)
            .then(res => res.json())
            .then(data => {
                product.disabled = false;
                data.forEach(p => {
                    product.innerHTML += `<option value="${p.id}">${p.name}</option>`;
                });
            });
    } else if (range === "Cosmetic") {
        // Fetch subcategories first
        subcategory.innerHTML = `<option value="" disabled selected>Select sub category</option>`;
        subcategory.disabled = false;

        fetch(`/subcategories/${catId}/`)
            .then(res => res.json())
            .then(data => {
                subcategory.innerHTML = `<option value="" disabled selected>Select sub category</option>`;
                data.forEach(sc => {
                    subcategory.innerHTML += `<option value="${sc.id}">${sc.type}</option>`;
                });
            });
    }
    });

    subcategory.addEventListener("change", function() {
    const range = productRange.value;
    const catId = category.value;
    const subcatId = subcategory.value;

    product.disabled = true;
    product.innerHTML = `<option value="" disabled selected>Select product</option>`;

    fetch(`/products/?category=${catId}&subcategory=${subcatId}&range=${range}`)
        .then(res => res.json())
        .then(data => {
            product.disabled = false;
            data.forEach(p => {
                product.innerHTML += `<option value="${p.id}">${p.name}</option>`;
            });
        });
    });



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

