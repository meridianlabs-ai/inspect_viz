// Modal dialog utilities for error display

export interface ModalOptions {
    title?: string;
    friendlyMessage: string;
    technicalMessage: string;
}

export class Modal {
    private static modalCSSInjected = false;

    static show(options: ModalOptions): void {
        const { title = 'Error', friendlyMessage, technicalMessage } = options;
        
        Modal.ensureModalCSS();
        const modal = Modal.createModal(friendlyMessage, technicalMessage, title);
        document.body.appendChild(modal);

        // Force a reflow to ensure initial styles are applied
        modal.offsetHeight;

        // Show with animation after initial render
        requestAnimationFrame(() => {
            requestAnimationFrame(() => {
                modal.classList.add('inspect-viz-modal-show');
                Modal.focusModal(modal);
            });
        });
    }

    private static ensureModalCSS(): void {
        if (Modal.modalCSSInjected || document.getElementById('inspect-viz-modal-css')) {
            return;
        }

        const style = document.createElement('style');
        style.id = 'inspect-viz-modal-css';
        style.textContent = `
            .inspect-viz-modal {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.5);
                display: flex;
                align-items: flex-start;
                justify-content: center;
                padding-top: 60px;
                z-index: 10000;
                opacity: 0;
                visibility: hidden;
                transition: opacity 0.3s, visibility 0.3s;
            }
            
            .inspect-viz-modal-show {
                opacity: 1;
                visibility: visible;
            }
            
            .inspect-viz-modal-content {
                background: white;
                border-radius: 8px;
                padding: 24px;
                min-width: 600px;
                max-width: min(90vw, 1000px);
                width: auto;
                max-height: calc(100vh - 120px);
                overflow-y: auto;
                box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
                position: relative;
                transform: translateY(-20px);
                transition: transform 0.3s ease-out;
            }
            
            .inspect-viz-modal-show .inspect-viz-modal-content {
                transform: translateY(0);
            }
            
            .inspect-viz-modal-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 16px;
                padding-bottom: 12px;
                border-bottom: 1px solid #e0e0e0;
            }

            .inspect-viz-modal-header h2 {
                border-bottom: none;
                padding-bottom: 0;
            }
            
            .inspect-viz-modal-title {
                font-size: 18px;
                font-weight: 600;
                color: #d32f2f;
                margin: 0;
                display: flex;
                align-items: center;
            }
            
            .inspect-viz-modal-icon {
                width: 20px;
                height: 20px;
                margin-right: 8px;
                fill: currentColor;
            }
            
            .inspect-viz-modal-close {
                background: none;
                border: none;
                font-size: 24px;
                cursor: pointer;
                padding: 0;
                width: 30px;
                height: 30px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 4px;
                color: #666;
            }
            
            .inspect-viz-modal-close:hover {
                background: #f5f5f5;
            }
            
            .inspect-viz-modal-close:focus {
                outline: 2px solid #1976d2;
                outline-offset: 2px;
            }
            
            .inspect-viz-modal-body {
                margin-bottom: 20px;
            }
            
            .inspect-viz-modal-message {
                font-size: 14px;
                line-height: 1.5;
                color: #333;
                margin-bottom: 16px;
            }
            
            .inspect-viz-modal-details {
                border: 1px solid #e0e0e0;
                border-radius: 4px;
            }
            
            .inspect-viz-modal-details summary {
                padding: 8px 12px;
                cursor: pointer;
                font-size: 13px;
                color: #666;
                background: #f8f9fa;
                border-radius: 4px 4px 0 0;
            }
            
            .inspect-viz-modal-details summary:hover {
                background: #e9ecef;
            }
            
            .inspect-viz-modal-details[open] summary {
                border-bottom: 1px solid #e0e0e0;
                border-radius: 4px 4px 0 0;
            }
            
            .inspect-viz-modal-details pre {
                margin: 0;
                padding: 12px;
                font-size: 12px;
                background: #f8f9fa;
                border-radius: 0 0 4px 4px;
                overflow-x: hidden;
                overflow-y: auto;
                color: #666;
                font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, Courier, monospace;
                white-space: pre-wrap;
                word-break: break-all;
                overflow-wrap: break-word;
                max-width: 100%;
                box-sizing: border-box;
            }
            
            .inspect-viz-modal-footer {
                text-align: right;
            }
            
            .inspect-viz-modal-button {
                background: #1976d2;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                cursor: pointer;
                font-size: 14px;
                font-family: inherit;
            }
            
            .inspect-viz-modal-button:hover {
                background: #1565c0;
            }
            
            .inspect-viz-modal-button:focus {
                outline: 2px solid #1976d2;
                outline-offset: 2px;
            }
            
            @media (max-width: 768px) {
                .inspect-viz-modal {
                    padding-top: 20px;
                }
                
                .inspect-viz-modal-content {
                    margin: 0 20px;
                    min-width: auto;
                    width: auto;
                    max-height: calc(100vh - 40px);
                }
            }
            
            @media (prefers-reduced-motion: reduce) {
                .inspect-viz-modal {
                    transition: none;
                }
            }
        `;
        document.head.appendChild(style);
        Modal.modalCSSInjected = true;
    }

    private static createModal(friendlyMessage: string, technicalMessage: string, title: string): HTMLElement {
        const modalHtml = `
            <div class="inspect-viz-modal" role="dialog" aria-labelledby="inspect-viz-modal-title" aria-modal="true">
                <div class="inspect-viz-modal-content">
                    <div class="inspect-viz-modal-header">
                        <h2 class="inspect-viz-modal-title" id="inspect-viz-modal-title">
                            <svg class="inspect-viz-modal-icon" viewBox="0 0 24 24">
                                <path d="M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z"/>
                            </svg>
                            ${Modal.escapeHtml(title)}
                        </h2>
                        <button class="inspect-viz-modal-close" aria-label="Close dialog">×</button>
                    </div>
                    <div class="inspect-viz-modal-body">
                        <div class="inspect-viz-modal-message">${Modal.escapeHtml(friendlyMessage)}</div>
                        <details class="inspect-viz-modal-details">
                            <summary>Technical Details</summary>
                            <pre>${Modal.escapeHtml(technicalMessage)}</pre>
                        </details>
                    </div>
                    <div class="inspect-viz-modal-footer">
                        <button class="inspect-viz-modal-button">Close</button>
                    </div>
                </div>
            </div>
        `;

        const div = document.createElement('div');
        div.innerHTML = modalHtml;
        const modal = div.firstElementChild as HTMLElement;

        // Add event listeners
        const closeButton = modal.querySelector('.inspect-viz-modal-close');
        const closeFooterButton = modal.querySelector('.inspect-viz-modal-button');
        const backdrop = modal;

        const closeModal = () => {
            modal.classList.remove('inspect-viz-modal-show');
            // Wait for animation to complete before removing from DOM
            setTimeout(() => {
                if (modal.parentNode) {
                    modal.parentNode.removeChild(modal);
                }
            }, 300);
        };

        closeButton?.addEventListener('click', closeModal);
        closeFooterButton?.addEventListener('click', closeModal);
        
        // Close on backdrop click
        backdrop.addEventListener('click', (e) => {
            if (e.target === backdrop) {
                closeModal();
            }
        });

        // Close on Escape key
        const handleKeyDown = (e: KeyboardEvent) => {
            if (e.key === 'Escape') {
                closeModal();
                document.removeEventListener('keydown', handleKeyDown);
            }
        };
        document.addEventListener('keydown', handleKeyDown);

        return modal;
    }

    private static focusModal(modal: HTMLElement): void {
        const closeButton = modal.querySelector('.inspect-viz-modal-close') as HTMLElement;
        if (closeButton) {
            closeButton.focus();
        }
    }

    private static escapeHtml(text: string): string {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}