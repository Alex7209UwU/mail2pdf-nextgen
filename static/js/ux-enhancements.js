/**
 * UX Enhancement System - Mail2PDF NextGen v2.0.0
 * Toast notifications, enhanced progress tracking, tooltips
 */

// ========================================
// TOAST NOTIFICATION SYSTEM
// ========================================

const ToastSystem = {
    container: null,

    init() {
        if (!this.container) {
            this.container = document.createElement('div');
            this.container.className = 'toast-container';
            document.body.appendChild(this.container);
        }
    },

    show(message, type = 'info', duration = 4000) {
        this.init();

        const toast = document.createElement('div');
        toast.className = `toast ${type}`;

        const icons = {
            success: '✓',
            error: '✕',
            warning: '⚠',
            info: 'ℹ'
        };

        toast.innerHTML = `
            <span class="toast-icon">${icons[type] || icons.info}</span>
            <div class="toast-content">${message}</div>
            <button class="toast-close" onclick="ToastSystem.remove(this.parentElement)">×</button>
        `;

        this.container.appendChild(toast);

        // Auto-remove after duration
        if (duration > 0) {
            setTimeout(() => this.remove(toast), duration);
        }

        return toast;
    },

    remove(toast) {
        toast.classList.add('removing');
        setTimeout(() => {
            if (toast.parentElement) {
                toast.parentElement.removeChild(toast);
            }
        }, 300);
    },

    success(message, duration) {
        return this.show(message, 'success', duration);
    },

    error(message, duration) {
        return this.show(message, 'error', duration);
    },

    warning(message, duration) {
        return this.show(message, 'warning', duration);
    },

    info(message, duration) {
        return this.show(message, 'info', duration);
    }
};

// ========================================
// ENHANCED PROGRESS TRACKER
// ========================================

const ProgressTracker = {
    current: 0,
    total: 0,
    startTime: null,
    currentFile: '',

    start(totalFiles) {
        this.total = totalFiles;
        this.current = 0;
        this.startTime = Date.now();
        this.update();
    },

    update(currentFile = '') {
        this.currentFile = currentFile;

        const percentage = this.total > 0 ? Math.round((this.current / this.total) * 100) : 0;
        const elapsed = (Date.now() - this.startTime) / 1000;
        const avgTimePerFile = this.current > 0 ? elapsed / this.current : 0;
        const remaining = (this.total - this.current) * avgTimePerFile;

        // Update progress bar
        const progressFill = document.getElementById('progressFill');
        if (progressFill) {
            progressFill.style.width = percentage + '%';
        }

        // Update progress info
        const progressContainer = document.getElementById('progressContainer');
        if (progressContainer) {
            let infoHtml = `
                <div class="progress-wrapper">
                    <div class="progress-info">
                        <span><span class="progress-percentage">${percentage}%</span> (${this.current}/${this.total} fichiers)</span>
                        ${remaining > 0 ? `<span class="progress-eta">~${Math.ceil(remaining)}s restantes</span>` : ''}
                    </div>
                    ${this.currentFile ? `<div class="progress-file">📄 ${this.currentFile}</div>` : ''}
                    <div class="progress-bar">
                        <div class="progress-fill" id="progressFill" style="width: ${percentage}%"></div>
                    </div>
                </div>
            `;
            progressContainer.innerHTML = infoHtml;
        }
    },

    increment(fileName = '') {
        this.current++;
        this.update(fileName);
    },

    complete() {
        this.current = this.total;
        this.update();
        ToastSystem.success(`✅ Conversion terminée ! ${this.total} fichier(s) traité(s).`);
    }
};

// ========================================
// TOOLTIP HELPER
// ========================================

function addTooltip(element, text) {
    element.classList.add('tooltip');
    const tooltipText = document.createElement('span');
    tooltipText.className = 'tooltiptext';
    tooltipText.textContent = text;
    element.appendChild(tooltipText);
}

// ========================================
// RETRY MECHANISM
// ========================================

const RetrySystem = {
    failedFiles: new Map(),

    addFailure(fileName, errorMessage, fileData) {
        this.failedFiles.set(fileName, {
            error: errorMessage,
            data: fileData,
            timestamp: new Date()
        });
    },

    async retry(fileName) {
        const failure = this.failedFiles.get(fileName);
        if (!failure) {
            ToastSystem.error(`Fichier non trouvé: ${fileName}`);
            return;
        }

        ToastSystem.info(`🔄 Nouvelle tentative: ${fileName}...`);

        try {
            const formData = new FormData();
            formData.append('files', failure.data);

            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (response.ok && result.results[0]?.status === 'success') {
                ToastSystem.success(`✅ ${fileName} converti avec succès !`);
                this.failedFiles.delete(fileName);
                return true;
            } else {
                ToastSystem.error(`❌ Échec: ${result.results[0]?.error || 'Erreur inconnue'}`);
                return false;
            }
        } catch (error) {
            ToastSystem.error(`❌ Erreur réseau: ${error.message}`);
            return false;
        }
    },

    createRetryButton(fileName) {
        const btn = document.createElement('button');
        btn.className = 'retry-btn';
        btn.textContent = '🔄 Réessayer';
        btn.onclick = () => this.retry(fileName);
        return btn;
    },

    createErrorDetails(errorMessage) {
        const details = document.createElement('div');
        details.className = 'error-details';
        details.style.display = 'none';
        details.textContent = errorMessage;

        const toggle = document.createElement('span');
        toggle.className = 'expand-error';
        toggle.textContent = 'Voir détails';
        toggle.onclick = () => {
            const isHidden = details.style.display === 'none';
            details.style.display = isHidden ? 'block' : 'none';
            toggle.textContent = isHidden ? 'Masquer détails' : 'Voir détails';
        };

        const wrapper = document.createElement('div');
        wrapper.appendChild(toggle);
        wrapper.appendChild(details);

        return wrapper;
    }
};

// ========================================
// PREVIEW SYSTEM
// ========================================

const PreviewSystem = {
    modal: null,

    init() {
        if (this.modal) return;

        // Create modal HTML
        const modalDiv = document.createElement('div');
        modalDiv.id = 'previewModal';
        modalDiv.className = 'modal hidden';
        modalDiv.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <div class="modal-title">Prévisualisation</div>
                    <button class="close-modal" onclick="PreviewSystem.close()">×</button>
                </div>
                <div class="modal-body">
                    <iframe id="previewFrame" class="modal-iframe"></iframe>
                </div>
            </div>
        `;
        document.body.appendChild(modalDiv);
        this.modal = modalDiv;

        // Close on click outside
        this.modal.addEventListener('click', (e) => {
            if (e.target === this.modal) {
                this.close();
            }
        });

        // Close on Escape
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && !this.modal.classList.contains('hidden')) {
                this.close();
            }
        });
    },

    async open(file) {
        this.init();

        const frame = document.getElementById('previewFrame');
        const title = this.modal.querySelector('.modal-title');

        // Show loading state
        this.modal.classList.remove('hidden');
        title.textContent = `Chargement: ${file.name}...`;
        frame.srcdoc = `
            <div style="font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100%; color: #666;">
                <div style="text-align: center;">
                    <div style="font-size: 24px; margin-bottom: 10px;">⌛</div>
                    <div>Chargement de l'aperçu...</div>
                </div>
            </div>
        `;

        try {
            const formData = new FormData();
            formData.append('file', file);

            const response = await fetch('/api/preview', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (response.ok && result.html) {
                title.textContent = `Aperçu: ${file.name}`;
                frame.srcdoc = result.html;
            } else {
                throw new Error(result.error || 'Erreur inconnue');
            }

        } catch (error) {
            title.textContent = 'Erreur';
            frame.srcdoc = `
                <div style="font-family: sans-serif; padding: 20px; color: #d63031; text-align: center;">
                    <h3>Erreur de prévisualisation</h3>
                    <p>${error.message}</p>
                </div>
            `;
            ToastSystem.error(`Erreur prévisualisation: ${error.message}`);
        }
    },

    close() {
        if (this.modal) {
            this.modal.classList.add('hidden');
            document.getElementById('previewFrame').srcdoc = '';
        }
    }
};

// ========================================
// KEYBOARD SHORTCUTS
// ========================================

document.addEventListener('DOMContentLoaded', () => {
    document.addEventListener('keydown', (e) => {
        // Ctrl+O: Open file dialog
        if (e.ctrlKey && e.key === 'o') {
            e.preventDefault();
            document.getElementById('fileInput')?.click();
        }

        // Ctrl+Enter: Start conversion
        if (e.ctrlKey && e.key === 'Enter') {
            e.preventDefault();
            document.getElementById('convertButton')?.click();
        }

        // Ctrl+D: Download results
        if (e.ctrlKey && e.key === 'd') {
            e.preventDefault();
            document.getElementById('downloadButton')?.click();
        }

        // ?: Show help
        if (e.shiftKey && e.key === '?') {
            showKeyboardShortcuts();
        }
    });
});

function showKeyboardShortcuts() {
    const shortcuts = `
        <strong>Raccourcis Clavier:</strong><br>
        Ctrl+O: Ouvrir fichier<br>
        Ctrl+Enter: Convertir<br>
        Ctrl+D: Télécharger<br>
        ?: Afficher cette aide
    `;
    ToastSystem.info(shortcuts, 8000);
}

};

// ========================================
// HISTORY SYSTEM
// ========================================

const HistorySystem = {
    modal: null,

    init() {
        if (this.modal) return;

        const modalDiv = document.createElement('div');
        modalDiv.id = 'historyModal';
        modalDiv.className = 'modal hidden';
        modalDiv.innerHTML = `
            <div class="modal-content" style="max-width: 800px;">
                <div class="modal-header">
                    <div class="modal-title">Historique des Conversions</div>
                    <button class="close-modal" onclick="HistorySystem.close()">×</button>
                </div>
                <div class="modal-body" style="padding: 20px;">
                    <div id="historyList" class="history-list">Chargement...</div>
                </div>
            </div>
        `;
        document.body.appendChild(modalDiv);
        this.modal = modalDiv;

        this.modal.addEventListener('click', (e) => {
            if (e.target === this.modal) this.close();
        });

        // Close on Escape
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && !this.modal.classList.contains('hidden')) {
                this.close();
            }
        });
    },

    async open() {
        this.init();
        this.modal.classList.remove('hidden');
        const list = document.getElementById('historyList');
        list.innerHTML = '<div class="text-center">Chargement...</div>';

        try {
            const response = await fetch('/api/history');
            const history = await response.json();

            if (history.length === 0) {
                list.innerHTML = '<div class="text-center" style="padding: 30px; color: #666;">Aucune conversion passée trouvée.</div>';
                return;
            }

            let html = '<table class="history-table"><thead><tr><th>Date</th><th>Fichiers</th><th>État</th><th>Actions</th></tr></thead><tbody>';

            history.forEach(session => {
                const date = new Date(session.timestamp).toLocaleString();

                html += `
                    <tr>
                        <td>${date}</td>
                        <td>${session.files_processed} fichier(s)</td>
                        <td>
                            <span style="color: var(--success-color)">${session.files_success} ✓</span>
                            ${session.files_failed > 0 ? `<span style="color: var(--warning-color); margin-left:10px;">${session.files_failed} ✕</span>` : ''}
                        </td>
                        <td>
                            <button class="action-btn" onclick="window.location.href='/api/download/${session.session_id}'" title="Télécharger">⬇️</button>
                        </td>
                    </tr>
                `;
            });

            html += '</tbody></table>';
            list.innerHTML = html;

        } catch (error) {
            list.innerHTML = `<div class="error-msg">Erreur de chargement: ${error.message}</div>`;
        }
    },

    close() {
        if (this.modal) this.modal.classList.add('hidden');
    }
};

// ========================================
// EXPORT FOR GLOBAL USE
// ========================================

window.ToastSystem = ToastSystem;
window.ProgressTracker = ProgressTracker;
window.RetrySystem = RetrySystem;
window.PreviewSystem = PreviewSystem;
window.HistorySystem = HistorySystem;
window.addTooltip = addTooltip;
