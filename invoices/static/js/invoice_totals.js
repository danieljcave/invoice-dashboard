document.addEventListener("DOMContentLoaded", function () {
    function calculateTotal() {
        let total = 0;
        document.querySelectorAll('.line-item-row').forEach(function (row) {
            const quantityField = row.querySelector('.field-quantity input');
            const unitPriceField = row.querySelector('.field-unit_price input');
            
            const quantity = parseFloat(quantityField ? quantityField.value : 0) || 0;
            const unitPrice = parseFloat(unitPriceField ? unitPriceField.value : 0) || 0;
            
            // Calculate the line item total and add it to the overall total
            total += quantity * unitPrice;
        });
        
        // Set the calculated total to the Total Amount field
        const totalAmountField = document.querySelector('#id_total_amount');
        if (totalAmountField) {
            totalAmountField.value = total.toFixed(2);
        }
    }

    // Attach event listeners to each line item input for real-time updates
    document.querySelectorAll('.line-item-row input').forEach(function (input) {
        input.addEventListener('input', calculateTotal);
    });

    // Initial calculation on page load
    calculateTotal();
});
