// Quantum Solver Suite JavaScript Application

$(document).ready(function() {
    // Initialize tooltips
    $('[data-bs-toggle="tooltip"]').tooltip();
    
    // Initialize popovers
    $('[data-bs-toggle="popover"]').popover();
    
    // Add loading states to buttons
    addLoadingStates();
    
    // Add parameter validation
    addParameterValidation();
    
    // Add keyboard shortcuts
    addKeyboardShortcuts();
    
    // Initialize theme switcher (if exists)
    initializeTheme();
});

function addLoadingStates() {
    // Add loading spinner functionality
    $(document).on('click', '.btn[type="submit"]', function() {
        const btn = $(this);
        const originalText = btn.html();
        
        btn.prop('disabled', true);
        btn.html('<span class="spinner-border spinner-border-sm me-2" role="status"></span>Solving...');
        
        // Restore button after timeout (fallback)
        setTimeout(function() {
            btn.prop('disabled', false);
            btn.html(originalText);
        }, 30000);
    });
}

function addParameterValidation() {
    // Real-time parameter validation
    $(document).on('input', 'input[type="number"]', function() {
        const input = $(this);
        const min = parseFloat(input.attr('min'));
        const max = parseFloat(input.attr('max'));
        const value = parseFloat(input.val());
        
        // Remove previous validation classes
        input.removeClass('is-valid is-invalid');
        
        if (isNaN(value)) {
            input.addClass('is-invalid');
            return;
        }
        
        if ((min !== undefined && value < min) || (max !== undefined && value > max)) {
            input.addClass('is-invalid');
            showParameterWarning(input, min, max);
        } else {
            input.addClass('is-valid');
            hideParameterWarning(input);
        }
    });
}

function showParameterWarning(input, min, max) {
    const warningId = `warning-${input.attr('id')}`;
    
    // Remove existing warning
    $(`#${warningId}`).remove();
    
    // Create warning message
    let message = 'Value out of range: ';
    if (min !== undefined && max !== undefined) {
        message += `should be between ${min} and ${max}`;
    } else if (min !== undefined) {
        message += `should be at least ${min}`;
    } else if (max !== undefined) {
        message += `should be at most ${max}`;
    }
    
    const warning = $(`<div id="${warningId}" class="text-danger small mt-1">${message}</div>`);
    input.parent().append(warning);
}

function hideParameterWarning(input) {
    const warningId = `warning-${input.attr('id')}`;
    $(`#${warningId}`).remove();
}

function addKeyboardShortcuts() {
    // Ctrl+Enter to solve
    $(document).on('keydown', function(e) {
        if (e.ctrlKey && e.which === 13) { // Ctrl+Enter
            e.preventDefault();
            $('#solve-btn').click();
        }
    });
    
    // Escape to clear results
    $(document).on('keydown', function(e) {
        if (e.which === 27) { // Escape
            clearResults();
        }
    });
}

function clearResults() {
    $('#results-container').hide();
    $('#welcome-message').show();
}

function initializeTheme() {
    // Check for saved theme preference
    const savedTheme = localStorage.getItem('quantum-solver-theme') || 'light';
    setTheme(savedTheme);
    
    // Add theme toggle button if it exists
    $(document).on('click', '.theme-toggle', function() {
        const currentTheme = $('body').attr('data-theme') || 'light';
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        setTheme(newTheme);
    });
}

function setTheme(theme) {
    $('body').attr('data-theme', theme);
    localStorage.setItem('quantum-solver-theme', theme);
    
    // Update theme toggle icon if it exists
    const icon = $('.theme-toggle i');
    if (theme === 'dark') {
        icon.removeClass('fa-moon').addClass('fa-sun');
    } else {
        icon.removeClass('fa-sun').addClass('fa-moon');
    }
}

// Enhanced result display functions
function displayResults(response) {
    const results = response.results;
    let html = '';
    
    // System Information Card
    if (results.system_info) {
        html += createSystemInfoCard(results.system_info);
    }
    
    // Results based on solver type
    if (results.bound_states) {
        html += createBoundStatesTable(results.bound_states);
    }
    
    if (results.energy_levels) {
        html += createEnergyLevelsTable(results.energy_levels);
    }
    
    if (results.tunneling_results) {
        html += createTunnelingResults(results.tunneling_results);
    }
    
    if (results.wave_numbers) {
        html += createWaveNumbersCard(results.wave_numbers);
    }
    
    // Display results
    $('#results-content').html(html);
    $('#results-container').show();
    $('#welcome-message').hide();
    
    // Display plot
    if (response.plot) {
        $('#plot-image').attr('src', response.plot).show();
    }
    
    // Add animations
    $('#results-container').addClass('fade-in-up');
    
    // Scroll to results
    $('html, body').animate({
        scrollTop: $('#results-container').offset().top - 100
    }, 500);
}

function createSystemInfoCard(systemInfo) {
    let html = '<div class="card mb-3 border-info">';
    html += '<div class="card-header bg-info text-white">';
    html += '<h6 class="mb-0"><i class="fas fa-info-circle me-2"></i>System Information</h6>';
    html += '</div>';
    html += '<div class="card-body">';
    html += '<div class="row">';
    
    Object.entries(systemInfo).forEach(([key, value]) => {
        const displayKey = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
        html += `<div class="col-md-6 mb-2">
                    <strong class="text-info">${displayKey}:</strong> 
                    <span class="font-monospace">${value}</span>
                 </div>`;
    });
    
    html += '</div></div></div>';
    return html;
}

function createBoundStatesTable(boundStates) {
    if (!boundStates || boundStates.length === 0) {
        return `<div class="alert alert-warning" role="alert">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    No bound states found for these parameters.
                </div>`;
    }
    
    let html = '<div class="card mb-3 border-success">';
    html += '<div class="card-header bg-success text-white">';
    html += '<h6 class="mb-0"><i class="fas fa-layer-group me-2"></i>Bound States</h6>';
    html += '</div>';
    html += '<div class="card-body">';
    html += '<div class="table-responsive">';
    html += '<table class="table table-hover mb-0">';
    html += '<thead class="table-dark">';
    html += '<tr><th>State</th><th>z-value</th><th>Energy</th><th>Binding Energy</th><th>Penetration</th></tr>';
    html += '</thead><tbody>';
    
    boundStates.forEach((state, index) => {
        const rowClass = index % 2 === 0 ? '' : 'table-light';
        html += `<tr class="${rowClass}">
                    <td><strong>n = ${state.state_number}</strong></td>
                    <td><code>${state.z_value}</code></td>
                    <td><code>${state.energy}</code></td>
                    <td><code>${state.binding_energy}</code></td>
                    <td><code>${state.penetration_depth || 'N/A'}</code></td>
                 </tr>`;
    });
    
    html += '</tbody></table></div></div></div>';
    return html;
}

function createEnergyLevelsTable(energyLevels) {
    let html = '<div class="card mb-3 border-primary">';
    html += '<div class="card-header bg-primary text-white">';
    html += '<h6 class="mb-0"><i class="fas fa-chart-line me-2"></i>Energy Levels</h6>';
    html += '</div>';
    html += '<div class="card-body">';
    html += '<div class="table-responsive">';
    html += '<table class="table table-hover mb-0">';
    html += '<thead class="table-dark">';
    html += '<tr><th>n</th><th>Energy</th>';
    
    // Add additional columns based on available data
    if (energyLevels[0] && energyLevels[0].degeneracy !== undefined) {
        html += '<th>Degeneracy</th>';
    }
    if (energyLevels[0] && energyLevels[0].classical_turning_points !== undefined) {
        html += '<th>Turning Points</th>';
    }
    if (energyLevels[0] && energyLevels[0].wavelength !== undefined) {
        html += '<th>Wavelength</th>';
    }
    if (energyLevels[0] && energyLevels[0].nodes !== undefined) {
        html += '<th>Nodes</th>';
    }
    
    html += '</tr></thead><tbody>';
    
    energyLevels.forEach((level, index) => {
        const rowClass = index % 2 === 0 ? '' : 'table-light';
        html += `<tr class="${rowClass}">
                    <td><strong>${level.n}</strong></td>
                    <td><code>${level.energy}</code></td>`;
        
        if (level.degeneracy !== undefined) {
            html += `<td><span class="badge bg-info">${level.degeneracy}</span></td>`;
        }
        if (level.classical_turning_points !== undefined) {
            html += `<td><code>±${level.classical_turning_points}</code></td>`;
        }
        if (level.wavelength !== undefined) {
            html += `<td><code>${level.wavelength}</code></td>`;
        }
        if (level.nodes !== undefined) {
            html += `<td>${level.nodes}</td>`;
        }
        
        html += '</tr>';
    });
    
    html += '</tbody></table></div></div></div>';
    return html;
}

function createTunnelingResults(tunnelingResults) {
    let html = '<div class="card mb-3 border-warning">';
    html += '<div class="card-header bg-warning text-dark">';
    html += '<h6 class="mb-0"><i class="fas fa-exchange-alt me-2"></i>Transmission & Reflection</h6>';
    html += '</div>';
    html += '<div class="card-body">';
    
    // Progress bars for transmission and reflection
    const transmissionPercent = tunnelingResults.transmission_probability;
    const reflectionPercent = tunnelingResults.reflection_probability;
    
    html += '<div class="row">';
    html += '<div class="col-md-6">';
    html += '<h6>Transmission</h6>';
    html += `<div class="progress mb-2">
                <div class="progress-bar bg-success" style="width: ${transmissionPercent}%">
                    ${transmissionPercent}%
                </div>
             </div>`;
    html += `<small class="text-muted">Coefficient: ${tunnelingResults.transmission_coefficient}</small>`;
    html += '</div>';
    
    html += '<div class="col-md-6">';
    html += '<h6>Reflection</h6>';
    html += `<div class="progress mb-2">
                <div class="progress-bar bg-danger" style="width: ${reflectionPercent}%">
                    ${reflectionPercent}%
                </div>
             </div>`;
    html += `<small class="text-muted">Coefficient: ${tunnelingResults.reflection_coefficient}</small>`;
    html += '</div>';
    html += '</div>';
    
    html += '</div></div>';
    return html;
}

function createWaveNumbersCard(waveNumbers) {
    let html = '<div class="card mb-3 border-secondary">';
    html += '<div class="card-header bg-secondary text-white">';
    html += '<h6 class="mb-0"><i class="fas fa-wave-square me-2"></i>Wave Properties</h6>';
    html += '</div>';
    html += '<div class="card-body">';
    html += '<div class="row">';
    
    Object.entries(waveNumbers).forEach(([key, value]) => {
        const displayKey = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
        html += `<div class="col-md-4 mb-2">
                    <strong>${displayKey}:</strong><br>
                    <code>${value}</code>
                 </div>`;
    });
    
    html += '</div></div></div>';
    return html;
}

// Enhanced example loading
function loadExample(solverId, exampleId) {
    // Show loading state
    const btn = $(`.example-btn[data-example-id="${exampleId}"]`);
    const originalText = btn.text();
    btn.prop('disabled', true).text('Loading...');
    
    $.get(`/api/example/${solverId}/${exampleId}`)
        .done(function(example) {
            // Populate form with example parameters
            Object.entries(example.parameters).forEach(([key, value]) => {
                const input = $(`#${key}`);
                input.val(value).trigger('input'); // Trigger validation
            });
            
            // Show success message
            showNotification('Example loaded successfully!', 'success');
        })
        .fail(function() {
            showNotification('Failed to load example', 'error');
        })
        .always(function() {
            btn.prop('disabled', false).text(originalText);
        });
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notificationId = `notification-${Date.now()}`;
    const alertClass = type === 'success' ? 'alert-success' : 
                     type === 'error' ? 'alert-danger' : 'alert-info';
    
    const notification = $(`
        <div id="${notificationId}" class="alert ${alertClass} alert-dismissible fade show position-fixed" 
             style="top: 20px; right: 20px; z-index: 9999; min-width: 300px;">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `);
    
    // Add to body
    $('body').append(notification);
    
    // Auto-dismiss after 3 seconds
    setTimeout(() => {
        notification.alert('close');
    }, 3000);
}

// Enhanced error handling
function handleSolverError(xhr) {
    let errorMessage = 'An unknown error occurred';
    
    if (xhr.responseJSON && xhr.responseJSON.error) {
        errorMessage = xhr.responseJSON.error;
    } else if (xhr.status === 0) {
        errorMessage = 'Connection failed. Please check your internet connection.';
    } else if (xhr.status >= 500) {
        errorMessage = 'Server error. Please try again later.';
    } else if (xhr.status === 404) {
        errorMessage = 'Solver not found.';
    }
    
    showNotification(errorMessage, 'error');
}

// Export functionality
function exportResults(format = 'json') {
    const resultsData = {
        timestamp: new Date().toISOString(),
        solver: window.currentSolverId,
        parameters: getFormParameters(),
        results: window.lastResults
    };
    
    if (format === 'json') {
        downloadJSON(resultsData, `quantum_results_${Date.now()}.json`);
    } else if (format === 'csv') {
        downloadCSV(resultsData, `quantum_results_${Date.now()}.csv`);
    }
}

function downloadJSON(data, filename) {
    const blob = new Blob([JSON.stringify(data, null, 2)], {type: 'application/json'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
}

function downloadCSV(data, filename) {
    // Convert results to CSV format (simplified)
    let csv = 'Parameter,Value\n';
    
    Object.entries(data.parameters).forEach(([key, value]) => {
        csv += `${key},${value}\n`;
    });
    
    csv += '\nResult,Value\n';
    
    // Add results (this would need to be customized per solver)
    if (data.results.bound_states) {
        data.results.bound_states.forEach((state, index) => {
            csv += `State ${index + 1} Energy,${state.energy}\n`;
        });
    }
    
    const blob = new Blob([csv], {type: 'text/csv'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
}

function getFormParameters() {
    const params = {};
    $('#solver-form').serializeArray().forEach(item => {
        params[item.name] = item.value;
    });
    return params;
}

// Add CSS animations
$('<style>').text(`
    .fade-in-up {
        animation: fadeInUp 0.5s ease-out;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .solver-card {
        transition: all 0.3s ease;
    }
    
    .solver-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .notification-enter {
        animation: slideInRight 0.3s ease-out;
    }
    
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
        }
        to {
            transform: translateX(0);
        }
    }
`).appendTo('head');
