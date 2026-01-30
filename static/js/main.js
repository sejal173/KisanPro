// Mobile Menu Toggle
document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    
    if (hamburger && navMenu) {
        hamburger.addEventListener('click', function() {
            navMenu.classList.toggle('active');
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', function(event) {
            if (!hamburger.contains(event.target) && !navMenu.contains(event.target)) {
                navMenu.classList.remove('active');
            }
        });
    }
    
    // Auto-hide flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(function(alert) {
        setTimeout(function() {
            alert.style.transition = 'opacity 0.5s';
            alert.style.opacity = '0';
            setTimeout(function() {
                alert.remove();
            }, 500);
        }, 5000);
    });
    
    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
    
    // Quantity input validation
    const quantityInputs = document.querySelectorAll('input[type="number"][name="quantity"]');
    quantityInputs.forEach(function(input) {
        input.addEventListener('change', function() {
            const max = parseInt(this.getAttribute('max'));
            const min = parseInt(this.getAttribute('min'));
            let value = parseInt(this.value);
            
            if (value > max) {
                this.value = max;
                alert('Maximum quantity available: ' + max);
            }
            if (value < min) {
                this.value = min;
            }
        });
    });
    
    // Cart total calculation (if needed for dynamic updates)
    updateCartTotal();
});

// Update cart total dynamically
function updateCartTotal() {
    const cartItems = document.querySelectorAll('.cart-table tbody tr');
    let total = 0;
    
    cartItems.forEach(function(row) {
        const quantityInput = row.querySelector('input[name="quantity"]');
        const priceText = row.querySelector('td:nth-child(2)').textContent;
        const price = parseFloat(priceText.replace('₹', '').replace('/kg', ''));
        const quantity = quantityInput ? parseInt(quantityInput.value) : 1;
        const itemTotal = price * quantity;
        
        // Update row total
        const totalCell = row.querySelector('td:nth-child(4)');
        if (totalCell) {
            totalCell.textContent = '₹' + itemTotal.toFixed(2);
        }
        
        total += itemTotal;
    });
    
    // Update summary total
    const summaryTotal = document.querySelector('.summary-row.total span:last-child');
    if (summaryTotal) {
        summaryTotal.textContent = '₹' + total.toFixed(2);
    }
}

// Filter seeds dynamically (if using AJAX)
function filterSeeds() {
    const cropType = document.getElementById('crop_type').value;
    const season = document.getElementById('season').value;
    
    // This would be used if implementing AJAX filtering
    // For now, the form submission handles filtering
}

// Confirm delete actions
function confirmDelete(message) {
    return confirm(message || 'Are you sure you want to delete this item?');
}

// Format currency
function formatCurrency(amount) {
    return '₹' + parseFloat(amount).toFixed(2);
}

// Show loading spinner
function showLoading() {
    const loader = document.createElement('div');
    loader.className = 'loader';
    loader.innerHTML = '<div class="spinner"></div>';
    document.body.appendChild(loader);
}

// Hide loading spinner
function hideLoading() {
    const loader = document.querySelector('.loader');
    if (loader) {
        loader.remove();
    }
}
