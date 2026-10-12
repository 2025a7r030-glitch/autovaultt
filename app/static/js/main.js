// AutoVault Main JavaScript Module — Luxury Black & Gold Cockpit UI

document.addEventListener('DOMContentLoaded', () => {
    // 1. Initialize Lucide Icons
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }

    // 2. Chart.js Executive Black & Gold Theme Defaults
    if (typeof Chart !== 'undefined') {
        Chart.defaults.color = '#c8cdd6';
        Chart.defaults.borderColor = 'rgba(212, 175, 55, 0.12)';
        Chart.defaults.font.family = "'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif";
        Chart.defaults.plugins.tooltip.backgroundColor = '#131419';
        Chart.defaults.plugins.tooltip.titleColor = '#f3d079';
        Chart.defaults.plugins.tooltip.bodyColor = '#ffffff';
        Chart.defaults.plugins.tooltip.borderColor = 'rgba(212, 175, 55, 0.35)';
        Chart.defaults.plugins.tooltip.borderWidth = 1;
        Chart.defaults.plugins.tooltip.padding = 10;
        Chart.defaults.plugins.tooltip.cornerRadius = 8;
    }

    // 3. Mobile Sidebar Toggle
    const mobileToggle = document.getElementById('mobileNavToggle');
    const sidebar = document.querySelector('.sidebar');
    if (mobileToggle && sidebar) {
        mobileToggle.addEventListener('click', () => {
            sidebar.classList.toggle('open');
        });
    }

    // 4. Modal Handlers
    window.openModal = function(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.add('active');
            if (typeof lucide !== 'undefined') {
                lucide.createIcons();
            }
        }
    };

    window.closeModal = function(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.remove('active');
        }
    };

    // Close modal when clicking on backdrop
    document.querySelectorAll('.modal-overlay').forEach(overlay => {
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) {
                overlay.classList.remove('active');
            }
        });
    });

    // 5. Alert notification dismissal
    document.querySelectorAll('.alert-close').forEach(btn => {
        btn.addEventListener('click', function() {
            const alert = this.closest('.alert');
            if (alert) {
                alert.style.opacity = '0';
                alert.style.transform = 'translateY(-6px)';
                setTimeout(() => alert.remove(), 220);
            }
        });
    });
});
