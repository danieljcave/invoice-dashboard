document.addEventListener('DOMContentLoaded', function() {
    function toggleCustomService(select) {
        let customServiceInput = select.closest('tr').querySelector('input[name$="-custom_service"]');
        if (select.value === '') {
            customServiceInput.style.display = 'inline';  // Show custom input if no dropdown option is selected
        } else {
            customServiceInput.style.display = 'none';  // Hide custom input when a dropdown option is selected
            customServiceInput.value = '';  // Clear custom input value when hidden
        }
    }

    document.querySelectorAll('select[name$="-service"]').forEach(function(select) {
        toggleCustomService(select);
        select.addEventListener('change', function() {
            toggleCustomService(select);
        });
    });

    // Apply this logic when new rows are added dynamically
    document.body.addEventListener('click', function(event) {
        if (event.target && event.target.matches('.add-row a')) {
            setTimeout(() => {
                document.querySelectorAll('select[name$="-service"]').forEach(function(select) {
                    if (!select.dataset.toggleApplied) {
                        toggleCustomService(select);
                        select.addEventListener('change', function() {
                            toggleCustomService(select);
                        });
                        select.dataset.toggleApplied = true;  // Mark as applied
                    }
                });
            }, 100);
        }
    });
});
