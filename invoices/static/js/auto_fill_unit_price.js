document.addEventListener('DOMContentLoaded', function() {
    function applyAutoFillLogic(select) {
        select.addEventListener('change', function() {
            let unitPriceInput = select.closest('tr').querySelector('input[name$="-unit_price"]');
            if (unitPriceInput) {
                if (select.value === 'Group Walk') {
                    unitPriceInput.value = '15.00';  // Auto set to 15 for Group Walk
                } else if (select.value === 'Pet Visit') {
                    unitPriceInput.value = '11.00';  // Auto set to 11 for Pet Visit
                } else if (select.value === 'Dog Sitting') {
                    unitPriceInput.value = '40.00';  // Auto set to 40 for Dog Sitting
                } else {
                    unitPriceInput.value = '';  // Clear if another option
                }
            }
        });
    }

    // Apply the logic to all existing service select elements on page load
    document.querySelectorAll('select[name$="-service"]').forEach(function(select) {
        applyAutoFillLogic(select);
    });

    // Observe changes to the document body for dynamically added nodes
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.addedNodes.length) {
                mutation.addedNodes.forEach(function(node) {
                    if (node.nodeType === 1) { // Check if the node is an element
                        const newSelect = node.querySelector('select[name$="-service"]');
                        if (newSelect && !newSelect.dataset.autoFillApplied) {
                            applyAutoFillLogic(newSelect);
                            newSelect.dataset.autoFillApplied = true;  // Mark as applied
                        }
                    }
                });
            }
        });
    });

    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
});
