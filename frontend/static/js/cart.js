document.addEventListener('DOMContentLoaded', function () {
    // Function to update the cart summary
    function updateCartSummary() {
        // Get all cart items
        const cartItems = document.querySelectorAll('.row.g-2.align-items-center');

        let totalProducts = 0;
        let subtotal = 0;

        // Loop through each cart item
        cartItems.forEach(item => {
            // Get the quantity and price of the current item
            const quantityInput = item.querySelector('input[name="quantity"]');
            let quantity = parseInt(quantityInput.value);

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
        });

        // Calculate shipping (example: 200 DZD for simplicity)
        const shipping = 200;

        // Calculate total amount
        const totalAmount = subtotal + shipping;

        // Update the DOM with the calculated values
        document.getElementById('products_count').textContent = totalProducts;
        document.getElementById('subtotal_count').textContent = `${subtotal.toFixed(2)} DZD`;
        document.getElementById('shipping_price').textContent = `${shipping.toFixed(2)} DZD`;
        document.getElementById('total_amount').textContent = `${totalAmount.toFixed(2)} DZD`;
    }

    // Call the function to update the cart summary when the page loads
    updateCartSummary();

    // Add event listeners to quantity inputs to update the cart summary when the quantity changes
    const quantityInputs = document.querySelectorAll('input[name="quantity"]');
    quantityInputs.forEach(input => {
        input.addEventListener('change', function () {
            // Ensure quantity is >= 1
            if (input.value < 1) {
                input.value = 1; // Reset to 1 if the value is less than 1
            }
            updateCartSummary();
        });
    });

    // Add event listener for remove buttons
    document.querySelectorAll('.delete-button').forEach(button => {
        button.addEventListener('click', function() {
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
});