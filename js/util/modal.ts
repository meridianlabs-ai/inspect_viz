// Modal dialog utilities for error display

export interface ModalOptions {
    title?: string;
    friendlyMessage: string;
    technicalMessage: string;
}

export class Modal {
    static show(options: ModalOptions): void {
        const { title = 'Error', friendlyMessage, technicalMessage } = options;

        // Check if we're in VS Code - if so, use console logging instead
        if (Modal.isVSCodeEnvironment()) {
            console.group(`🚨 ${title}`);
            console.error(friendlyMessage);
            console.groupCollapsed('Technical Details');
            console.error(technicalMessage);
            console.groupEnd();
            console.groupEnd();
            return;
        }

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

    private static createModal(
        friendlyMessage: string,
        technicalMessage: string,
        title: string
    ): HTMLElement {
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
        backdrop.addEventListener('click', e => {
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

    private static isVSCodeEnvironment(): boolean {
        // Check multiple indicators for VS Code environment
        return !!(
            document.querySelector('div[data-vscode-context]') ||
            document.body.classList.contains('vscode-body') ||
            window.location.href.includes('vscode-webview') ||
            navigator.userAgent.includes('VSCode') ||
            // Check for VS Code-specific global variables
            (window as any).acquireVsCodeApi
        );
    }
}
