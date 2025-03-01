langCode = document.documentElement.getAttribute('data-lang')


document.addEventListener('DOMContentLoaded', function () {
    // Function to update the cart summary
    function updateCartSummary(shipping = 0) {
        const cartItems = document.querySelectorAll('.cart_item');
        console.log('Function called, cart items found:', cartItems.length);

        let totalProducts = 0;
        let subtotal = 0;

        // Loop through each cart item
        cartItems.forEach(item => {
            // Get the quantity and price of the current item
            const quantityInput = item.querySelector('.item_quantity');
            let quantity = parseInt(quantityInput.innerText);

            // Ensure quantity is >= 1
            if (quantity < 1) {
                quantity = 1; // Reset to 1 if the value is less than 1
                quantityInput.value = 1; // Update the input field
            }

            const price = parseFloat(item.querySelector('.item_price').textContent
                .replace(' DZD', '')
                .replace(',', '.'));

            // Update total products and subtotal
            totalProducts += quantity;
            subtotal += quantity * price;
            console.log('subtotal');
            
        });

        // Calculate total amount
        const totalAmount = subtotal + shipping;

        // Update the DOM with the calculated values
        document.getElementById('products_count').textContent = totalProducts;
        document.getElementById('subtotal_count').textContent = `${subtotal.toFixed(2)} DZD`;
        document.getElementById('shipping_price').textContent = `${shipping.toFixed(2)} DZD`;
        document.getElementById('total_amount').textContent = `${totalAmount.toFixed(2)} DZD`;
    }

    // Call the function to update the cart summary when the page loads
    updateCartSummary(0);

    // Add event listener for remove buttons
    document.querySelectorAll('.delete-button').forEach(button => {
        button.addEventListener('click', function () {
            // Update to match server version
            const deleteUrl = this.dataset.deleteUrl;
            const csrfToken = this.dataset.csrfToken;

            // Send AJAX request to remove item
            fetch(deleteUrl, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json'
                }
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Remove the item from the DOM
                        this.closest('.container-fluid').remove();
                        updateCartSummary();
                    }
                })
                .catch(error => console.error('Error:', error));
        });
    });

    // Add this code to handle wilaya change
    document.getElementById('wilaya').addEventListener('change', async function () {
        const citySelect = document.getElementById('city');
        const wilayaCode = this.value;
        
        // Fix: Clear existing options before adding new ones
        citySelect.innerHTML = '<option value="">Select City</option>';

        if (wilayaCode) {
            try {
                // Fetch cities from backend
                const response = await fetch(`/dashboard/api/wilayas/${wilayaCode}/cities/`);

                if (!response.ok) {
                    throw new Error('Failed to fetch cities');
                }
                const cities = await response.json();

                // Add new city options
                cities.forEach(city => {
                    const option = document.createElement('option');
                    option.value = city.id;
                    if (langCode == 'ar') {
                        option.textContent = city.name_ar;
                    }
                    else {
                        option.textContent = city.name_fr;
                    }
                    citySelect.appendChild(option);
                });

                // Fetch shipping price for selected province
                const shippingResponse = await fetch(`/dashboard/shipping/getShippingPrice/${wilayaCode}/`);

                if (!shippingResponse.ok) {
                    throw new Error('Failed to fetch shipping price');
                }
                const shippingData = await shippingResponse.json();
                const price = shippingData.price && !isNaN(parseFloat(shippingData.price)) ?
                    parseFloat(shippingData.price) : 0;
                // Update shipping price element
                document.getElementById('shipping_price').textContent = `${price.toFixed(2)} DZD`;
                updateCartSummary(price);
            } catch (error) {
                console.error('Error:', error);
            }
        }
    });
});


