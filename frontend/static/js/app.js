/**
 * Email Classifier AI - Frontend JavaScript
 * Gerencia toda a interação da aplicação web
 */

class EmailClassifierApp {
    constructor() {
        this.apiBaseUrl = '/api';
        this.maxFileSize = 16 * 1024 * 1024; // 16MB
        this.allowedExtensions = ['txt', 'pdf'];
        this.currentRequest = null;
        
        this.init();
    }

    /**
     * Inicializa a aplicação
     */
    init() {
        this.setupEventListeners();
        this.setupDarkMode();
        this.setupTooltips();
        this.checkApiHealth();
        this.setupDragAndDrop();
        this.updateCharacterCount();
    }

    /**
     * Configura todos os event listeners
     */
    setupEventListeners() {
        // Formulários
        document.getElementById('textForm').addEventListener('submit', (e) => this.handleTextSubmit(e));
        document.getElementById('fileForm').addEventListener('submit', (e) => this.handleFileSubmit(e));
        
        // Dark mode toggle
        document.getElementById('darkModeToggle').addEventListener('change', (e) => this.toggleDarkMode(e));
        
        // Character counter
        document.getElementById('emailText').addEventListener('input', () => this.updateCharacterCount());
        
        // Results actions
        document.getElementById('copyResponseBtn').addEventListener('click', () => this.copyResponse());
        document.getElementById('clearResultsBtn').addEventListener('click', () => this.clearResults());
        document.getElementById('downloadResultsBtn').addEventListener('click', () => this.downloadResults());
        
        // File input change
        document.getElementById('fileUpload').addEventListener('change', (e) => this.handleFileSelection(e));
        
        // Tab changes
        document.querySelectorAll('#inputTabs button').forEach(tab => {
            tab.addEventListener('shown.bs.tab', () => this.clearForm());
        });
    }

    /**
     * Configura o dark mode
     */
    setupDarkMode() {
        const darkModeToggle = document.getElementById('darkModeToggle');
        const savedTheme = localStorage.getItem('theme') || 'light';
        
        document.documentElement.setAttribute('data-bs-theme', savedTheme);
        darkModeToggle.checked = savedTheme === 'dark';
        
        this.updateDarkModeIcon(savedTheme === 'dark');
    }

    /**
     * Alterna entre dark e light mode
     */
    toggleDarkMode(event) {
        const isDark = event.target.checked;
        const theme = isDark ? 'dark' : 'light';
        
        document.documentElement.setAttribute('data-bs-theme', theme);
        localStorage.setItem('theme', theme);
        
        this.updateDarkModeIcon(isDark);
        this.showToast('Tema alterado!', `Modo ${isDark ? 'escuro' : 'claro'} ativado`, 'success');
    }

    /**
     * Atualiza o ícone do dark mode
     */
    updateDarkModeIcon(isDark) {
        const icon = document.querySelector('#darkModeToggle + label i');
        icon.className = isDark ? 'bi bi-sun' : 'bi bi-moon-stars';
    }

    /**
     * Configura tooltips do Bootstrap
     */
    setupTooltips() {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    /**
     * Configura drag and drop para upload de arquivos
     */
    setupDragAndDrop() {
        const dropArea = document.getElementById('dropArea');
        const fileInput = document.getElementById('fileUpload');

        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropArea.addEventListener(eventName, this.preventDefaults, false);
        });

        ['dragenter', 'dragover'].forEach(eventName => {
            dropArea.addEventListener(eventName, () => dropArea.classList.add('dragover'), false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropArea.addEventListener(eventName, () => dropArea.classList.remove('dragover'), false);
        });

        dropArea.addEventListener('drop', (e) => this.handleDrop(e), false);
        dropArea.addEventListener('click', () => fileInput.click());
    }

    /**
     * Previne comportamentos padrão do drag and drop
     */
    preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    /**
     * Manipula o drop de arquivos
     */
    handleDrop(e) {
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            const fileInput = document.getElementById('fileUpload');
            fileInput.files = files;
            this.handleFileSelection({ target: fileInput });
        }
    }

    /**
     * Manipula a seleção de arquivos
     */
    handleFileSelection(event) {
        const file = event.target.files[0];
        if (!file) return;

        const validation = this.validateFile(file);
        if (!validation.valid) {
            this.showToast('Erro no arquivo', validation.message, 'error');
            event.target.value = '';
            return;
        }

        this.showToast('Arquivo selecionado', `${file.name} (${this.formatFileSize(file.size)})`, 'success');
    }

    /**
     * Valida o arquivo selecionado
     */
    validateFile(file) {
        // Verificar tamanho
        if (file.size > this.maxFileSize) {
            return {
                valid: false,
                message: `Arquivo muito grande. Máximo permitido: ${this.formatFileSize(this.maxFileSize)}`
            };
        }

        // Verificar extensão
        const extension = file.name.split('.').pop().toLowerCase();
        if (!this.allowedExtensions.includes(extension)) {
            return {
                valid: false,
                message: `Formato não permitido. Use: ${this.allowedExtensions.join(', ')}`
            };
        }

        return { valid: true };
    }

    /**
     * Formata o tamanho do arquivo
     */
    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    /**
     * Atualiza o contador de caracteres
     */
    updateCharacterCount() {
        const textArea = document.getElementById('emailText');
        const charCount = document.getElementById('charCount');
        const currentLength = textArea.value.length;
        const maxLength = 10000;

        charCount.textContent = currentLength.toLocaleString();
        
        // Mudar cor baseado no limite
        if (currentLength > maxLength * 0.9) {
            charCount.style.color = '#dc3545';
        } else if (currentLength > maxLength * 0.7) {
            charCount.style.color = '#ffc107';
        } else {
            charCount.style.color = '#667eea';
        }
    }

    /**
     * Manipula o submit do formulário de texto
     */
    async handleTextSubmit(event) {
        event.preventDefault();
        
        const emailText = document.getElementById('emailText').value.trim();
        if (!emailText) {
            this.showToast('Erro de validação', 'Por favor, digite o conteúdo do email', 'error');
            return;
        }

        await this.analyzeText(emailText);
    }

    /**
     * Manipula o submit do formulário de arquivo
     */
    async handleFileSubmit(event) {
        event.preventDefault();
        
        const fileInput = document.getElementById('fileUpload');
        const file = fileInput.files[0];
        
        if (!file) {
            this.showToast('Erro de validação', 'Por favor, selecione um arquivo', 'error');
            return;
        }

        const validation = this.validateFile(file);
        if (!validation.valid) {
            this.showToast('Erro no arquivo', validation.message, 'error');
            return;
        }

        await this.analyzeFile(file);
    }

    /**
     * Analisa texto diretamente
     */
    async analyzeText(text) {
        const formData = new FormData();
        formData.append('text', text);
        
        await this.sendAnalysisRequest(formData, 'text');
    }

    /**
     * Analisa arquivo
     */
    async analyzeFile(file) {
        const formData = new FormData();
        formData.append('file', file);
        
        await this.sendAnalysisRequest(formData, 'file');
    }

    /**
     * Envia requisição de análise para o backend
     */
    async sendAnalysisRequest(formData, type) {
        const submitBtn = document.querySelector(`#${type}Form .submit-btn`);
        
        try {
            this.setLoadingState(submitBtn, true);
            this.hideResults();

            // Cancelar requisição anterior se existir
            if (this.currentRequest) {
                this.currentRequest.abort();
            }

            // Criar nova requisição com AbortController
            const controller = new AbortController();
            this.currentRequest = controller;

            const response = await fetch(`${this.apiBaseUrl}/classify`, {
                method: 'POST',
                body: formData,
                signal: controller.signal
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Erro na análise');
            }

            this.displayResults(data);
            this.showToast('Análise concluída!', 'Email classificado com sucesso', 'success');

        } catch (error) {
            if (error.name === 'AbortError') {
                this.showToast('Análise cancelada', 'Requisição foi cancelada', 'info');
            } else {
                console.error('Erro na análise:', error);
                this.showToast('Erro na análise', error.message, 'error');
            }
        } finally {
            this.setLoadingState(submitBtn, false);
            this.currentRequest = null;
        }
    }

    /**
     * Define o estado de loading dos botões
     */
    setLoadingState(button, loading) {
        const spinner = button.querySelector('.spinner-border');
        const text = button.querySelector('.btn-text');
        
        if (loading) {
            button.classList.add('loading');
            button.disabled = true;
            spinner.classList.remove('d-none');
            text.textContent = 'Analisando...';
        } else {
            button.classList.remove('loading');
            button.disabled = false;
            spinner.classList.add('d-none');
            text.textContent = button.id.includes('file') ? 'Analisar Arquivo' : 'Analisar Email';
        }
    }

    /**
     * Exibe os resultados da análise
     */
    displayResults(data) {
        // Mostrar seção de resultados
        const resultsSection = document.getElementById('resultsSection');
        resultsSection.classList.remove('d-none');
        resultsSection.classList.add('fade-in');

        // Atualizar categoria
        this.updateCategoryDisplay(data.classification, data.confidence);

        // Atualizar resposta sugerida
        document.getElementById('suggestedResponse').textContent = data.suggested_response;

        // Atualizar preview do texto original
        document.getElementById('originalTextPreview').textContent = data.original_text;

        // Scroll para os resultados
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });

        // Salvar dados para download
        this.lastResults = data;
    }

    /**
     * Atualiza a exibição da categoria
     */
    updateCategoryDisplay(category, confidence) {
        const categoryBadge = document.getElementById('categoryBadge');
        const categoryText = document.getElementById('categoryText');
        const confidenceBar = document.getElementById('confidenceBar');
        const confidenceText = document.getElementById('confidenceText');

        // Atualizar texto da categoria
        categoryText.textContent = category;

        // Atualizar estilo da badge baseado na categoria
        categoryBadge.className = 'badge fs-6 py-2 px-3 mb-3';
        
        switch (category.toLowerCase()) {
            case 'produtivo':
                categoryBadge.classList.add('bg-success');
                break;
            case 'improdutivo':
                categoryBadge.classList.add('bg-danger');
                break;
            default:
                categoryBadge.classList.add('bg-warning');
                break;
        }

        // Atualizar barra de confiança
        const confidencePercent = Math.round(confidence * 100);
        confidenceBar.style.width = `${confidencePercent}%`;
        confidenceBar.setAttribute('aria-valuenow', confidencePercent);
        confidenceText.textContent = `${confidencePercent}%`;

        // Cor da barra baseada na confiança
        confidenceBar.className = 'progress-bar';
        if (confidencePercent >= 80) {
            confidenceBar.classList.add('bg-success');
        } else if (confidencePercent >= 60) {
            confidenceBar.classList.add('bg-warning');
        } else {
            confidenceBar.classList.add('bg-danger');
        }
    }

    /**
     * Copia a resposta sugerida
     */
    async copyResponse() {
        const responseText = document.getElementById('suggestedResponse').textContent;
        const copyBtn = document.getElementById('copyResponseBtn');

        try {
            await navigator.clipboard.writeText(responseText);
            
            // Feedback visual
            const originalContent = copyBtn.innerHTML;
            copyBtn.innerHTML = '<i class="bi bi-check-lg me-2"></i>Copiado!';
            copyBtn.classList.add('copied');
            
            setTimeout(() => {
                copyBtn.innerHTML = originalContent;
                copyBtn.classList.remove('copied');
            }, 2000);

            this.showToast('Sucesso!', 'Resposta copiada para a área de transferência', 'success');
        } catch (error) {
            this.showToast('Erro', 'Não foi possível copiar a resposta', 'error');
        }
    }

    /**
     * Limpa os resultados e formulários
     */
    clearResults() {
        // Esconder resultados
        this.hideResults();
        
        // Limpar formulários
        this.clearForm();
        
        // Cancelar requisição se ativa
        if (this.currentRequest) {
            this.currentRequest.abort();
        }

        this.showToast('Limpo!', 'Formulários e resultados foram limpos', 'info');
    }

    /**
     * Esconde a seção de resultados
     */
    hideResults() {
        const resultsSection = document.getElementById('resultsSection');
        resultsSection.classList.add('d-none');
        resultsSection.classList.remove('fade-in');
    }

    /**
     * Limpa todos os formulários
     */
    clearForm() {
        document.getElementById('emailText').value = '';
        document.getElementById('fileUpload').value = '';
        this.updateCharacterCount();
        
        // Remover classes de validação
        document.querySelectorAll('.form-control').forEach(control => {
            control.classList.remove('is-valid', 'is-invalid');
        });
    }

    /**
     * Faz download dos resultados
     */
    downloadResults() {
        if (!this.lastResults) {
            this.showToast('Erro', 'Nenhum resultado para download', 'error');
            return;
        }

        const results = {
            timestamp: new Date().toISOString(),
            classificacao: this.lastResults.classification,
            confianca: `${Math.round(this.lastResults.confidence * 100)}%`,
            resposta_sugerida: this.lastResults.suggested_response,
            texto_original: this.lastResults.original_text,
            texto_processado: this.lastResults.processed_text
        };

        const dataStr = JSON.stringify(results, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        
        const link = document.createElement('a');
        link.href = URL.createObjectURL(dataBlob);
        link.download = `analise_email_${new Date().toISOString().slice(0, 10)}.json`;
        link.click();

        this.showToast('Download!', 'Resultado salvo com sucesso', 'success');
    }

    /**
     * Verifica a saúde da API
     */
    async checkApiHealth() {
        const statusIndicator = document.getElementById('apiStatus');
        
        try {
            const response = await fetch(`${this.apiBaseUrl}/health`, {
                timeout: 5000
            });
            
            if (response.ok) {
                statusIndicator.className = 'badge bg-success';
                statusIndicator.innerHTML = '<i class="bi bi-check-circle me-1"></i>Online';
                statusIndicator.setAttribute('data-bs-original-title', 'API funcionando normalmente');
            } else {
                throw new Error('API com problemas');
            }
        } catch (error) {
            statusIndicator.className = 'badge bg-danger';
            statusIndicator.innerHTML = '<i class="bi bi-x-circle me-1"></i>Offline';
            statusIndicator.setAttribute('data-bs-original-title', 'API indisponível');
        }
    }

    /**
     * Mostra toast de notificação
     */
    showToast(title, message, type = 'info') {
        const toastContainer = document.getElementById('toastContainer');
        const toastId = `toast-${Date.now()}`;
        
        const iconMap = {
            success: 'bi-check-circle-fill',
            error: 'bi-x-circle-fill',
            warning: 'bi-exclamation-triangle-fill',
            info: 'bi-info-circle-fill'
        };

        const colorMap = {
            success: 'text-success',
            error: 'text-danger',
            warning: 'text-warning',
            info: 'text-primary'
        };

        const toastHtml = `
            <div id="${toastId}" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="toast-header">
                    <i class="bi ${iconMap[type]} ${colorMap[type]} me-2"></i>
                    <strong class="me-auto">${title}</strong>
                    <small>agora</small>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
                <div class="toast-body">
                    ${message}
                </div>
            </div>
        `;

        toastContainer.insertAdjacentHTML('beforeend', toastHtml);
        
        const toastElement = document.getElementById(toastId);
        const toast = new bootstrap.Toast(toastElement, {
            autohide: true,
            delay: type === 'error' ? 5000 : 3000
        });
        
        toast.show();

        // Remover do DOM após ocultar
        toastElement.addEventListener('hidden.bs.toast', () => {
            toastElement.remove();
        });
    }
}

// Inicializar aplicação quando DOM estiver carregado
document.addEventListener('DOMContentLoaded', () => {
    new EmailClassifierApp();
});

// Verificar health da API periodicamente
setInterval(() => {
    if (window.emailApp) {
        window.emailApp.checkApiHealth();
    }
}, 60000); // A cada minuto
