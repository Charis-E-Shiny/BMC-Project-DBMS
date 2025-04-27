// Function to confirm delete actions
function confirmDelete(event, type, name) {
    if (!confirm(`Are you sure you want to delete this ${type}: "${name}"?`)) {
        event.preventDefault();
        return false;
    }
    return true;
}

// Initialize tooltips
document.addEventListener('DOMContentLoaded', function() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Format numbers as currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 2
    }).format(amount);
}

// Toggle description visibility
function toggleDescription(id) {
    const description = document.getElementById(id);
    if (description.classList.contains('d-none')) {
        description.classList.remove('d-none');
    } else {
        description.classList.add('d-none');
    }
}

// Function to calculate business model totals
function calculateTotals() {
    // Revenue calculation
    const revenueElements = document.querySelectorAll('.revenue-amount');
    let totalRevenue = 0;
    revenueElements.forEach(element => {
        const amount = parseFloat(element.dataset.amount || 0);
        totalRevenue += amount;
    });
    
    // Cost calculation
    const costElements = document.querySelectorAll('.cost-amount');
    let totalCost = 0;
    costElements.forEach(element => {
        const amount = parseFloat(element.dataset.amount || 0);
        totalCost += amount;
    });
    
    // Profit calculation
    const profit = totalRevenue - totalCost;
    
    // Update display
    const revenueDisplay = document.getElementById('total-revenue');
    const costDisplay = document.getElementById('total-cost');
    const profitDisplay = document.getElementById('total-profit');
    
    if (revenueDisplay) revenueDisplay.textContent = formatCurrency(totalRevenue);
    if (costDisplay) costDisplay.textContent = formatCurrency(totalCost);
    if (profitDisplay) {
        profitDisplay.textContent = formatCurrency(profit);
        
        // Update profit color based on positive/negative
        if (profit > 0) {
            profitDisplay.classList.remove('text-danger');
            profitDisplay.classList.add('text-success');
        } else {
            profitDisplay.classList.remove('text-success');
            profitDisplay.classList.add('text-danger');
        }
    }
}

// Call calculation on page load if on the view or edit model page
document.addEventListener('DOMContentLoaded', function() {
    if (document.querySelector('.business-model-grid')) {
        calculateTotals();
    }
});
