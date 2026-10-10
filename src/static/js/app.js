function showToast(message, type = 'error') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    
    toast.className = `toast toast-${type} toast-enter`;
    toast.innerHTML = `
        <span>${message}</span>
        <button onclick="this.parentElement.remove()" class="ml-auto focus:outline-none">
            <svg class="w-4 h-4 opacity-75 hover:opacity-100" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
        </button>
    `;
    
    container.appendChild(toast);
    
    // Trigger animation
    requestAnimationFrame(() => {
        toast.classList.remove('toast-enter');
        toast.classList.add('toast-enter-active');
    });

    // Auto remove
    setTimeout(() => {
        toast.classList.add('toast-leave-active');
        setTimeout(() => toast.remove(), 300);
    }, 5000);
}

function appData() {
    return {
        activeTab: 'missing',
        loading: false,
        result: null,
        resultHtml: '',
        
        missingForm: { vin: null, vout: null, r1: null, r2: null },
        parallelForm: { target_value: null },
        dividerForm: { vin: null, vout: null, maximum_current: null },

        async submitRequest(url, payload, formatCallback) {
            this.loading = true;
            this.result = null;
            this.resultHtml = '';
            
            try {
                const response = await fetch(url, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                
                const data = await response.json();
                
                if (!response.ok) {
                    throw new Error(data.message || 'An error occurred');
                }
                
                this.result = data.data;
                this.resultHtml = formatCallback(data.data);
                
            } catch (error) {
                showToast(error.message, 'error');
            } finally {
                this.loading = false;
            }
        },

        calculateMissing() {
            // Clean payload
            const payload = {
                vin: this.missingForm.vin === '' ? null : this.missingForm.vin,
                vout: this.missingForm.vout === '' ? null : this.missingForm.vout,
                r1: this.missingForm.r1 === '' ? null : this.missingForm.r1,
                r2: this.missingForm.r2 === '' ? null : this.missingForm.r2,
            };
            
            this.submitRequest('/api/calculate-missing', payload, (data) => {
                return `
                    <div class="grid grid-cols-2 gap-4">
                        <div class="font-semibold capitalize">${data.calculated_parameter}:</div>
                        <div class="font-mono bg-white px-3 py-1 rounded border shadow-sm">${data.value.toFixed(4)}</div>
                    </div>
                `;
            });
        },

        calculateParallel() {
            this.submitRequest('/api/best-parallel', this.parallelForm, (data) => {
                return `
                    <div class="grid grid-cols-2 gap-y-3 gap-x-4">
                        <div class="font-semibold text-slate-600">Best R1:</div>
                        <div class="font-mono bg-white px-3 py-1 rounded border shadow-sm">${data.r1_shorthand} (${data.r1} Ω)</div>
                        
                        <div class="font-semibold text-slate-600">Best R2:</div>
                        <div class="font-mono bg-white px-3 py-1 rounded border shadow-sm">${data.r2_shorthand} (${data.r2} Ω)</div>
                        
                        <div class="font-semibold text-slate-600">Error:</div>
                        <div class="font-mono bg-white px-3 py-1 rounded border shadow-sm">${data.error.toFixed(4)} Ω</div>
                    </div>
                `;
            });
        },

        calculateDividerResistors() {
            this.submitRequest('/api/divider-resistors', this.dividerForm, (data) => {
                return `
                    <div class="grid grid-cols-2 gap-y-3 gap-x-4">
                        <div class="font-semibold text-slate-600">Best R1:</div>
                        <div class="font-mono bg-white px-3 py-1 rounded border shadow-sm">${data.r1_shorthand} (${data.r1} Ω)</div>
                        
                        <div class="font-semibold text-slate-600">Best R2:</div>
                        <div class="font-mono bg-white px-3 py-1 rounded border shadow-sm">${data.r2_shorthand} (${data.r2} Ω)</div>
                        
                        <div class="font-semibold text-slate-600">Error:</div>
                        <div class="font-mono bg-white px-3 py-1 rounded border shadow-sm">${data.error.toFixed(4)} V</div>
                        
                        <div class="font-semibold text-slate-600">Current:</div>
                        <div class="font-mono bg-white px-3 py-1 rounded border shadow-sm">${data.current_ma.toFixed(4)} mA</div>
                    </div>
                `;
            });
        }
    }
}
