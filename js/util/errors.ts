import { Modal } from './modal.js';

export function initializeErrorHandling(): void {
    const errorHandler = new ErrorHandler();

    // Handle unhandled errors (including worker errors)
    window.addEventListener('error', event => {
        const error = event.error;
        if (error) {
            const errorMessage = error.message || error.toString();
            const isSQL = isSQLError(errorMessage);
            errorHandler.handleError(errorMessage, isSQL);
        }
    });

    // Handle unhandled promise rejections
    window.addEventListener('unhandledrejection', event => {
        const error = event.reason;
        let errorMessage = '';

        if (error instanceof Error) {
            errorMessage = error.message;
        } else if (typeof error === 'string') {
            errorMessage = error;
        } else {
            errorMessage = String(error);
        }

        const isSQL = isSQLError(errorMessage);
        errorHandler.handleError(errorMessage, isSQL);

        // Prevent the default unhandled rejection behavior
        event.preventDefault();
    });
}

function isSQLError(message: string): boolean {
    const sqlErrorIndicators = [
        'Binder Error',
        'column "',
        'table "',
        'syntax error',
        'type mismatch',
        'division by zero',
        'conversion error',
        'SQL',
        'DuckDB',
    ];

    return sqlErrorIndicators.some(indicator =>
        message.toLowerCase().includes(indicator.toLowerCase())
    );
}

interface ErrorPattern {
    pattern: RegExp;
    message: (match: RegExpMatchArray) => string;
}

class ErrorHandler {
    private lastErrorTime = 0;
    private readonly ERROR_THROTTLE_MS = 2000; // Prevent spam

    handleError(errorMessage: string, isSQLError: boolean = false): void {
        // Throttle rapid errors
        const now = Date.now();
        if (now - this.lastErrorTime < this.ERROR_THROTTLE_MS) return;
        this.lastErrorTime = now;

        const friendlyError = isSQLError
            ? this.translateSqlError(errorMessage)
            : 'An unexpected error occurred in the application.';
        const errorTitle = isSQLError ? 'Query Error' : 'Application Error';

        Modal.show({
            title: errorTitle,
            friendlyMessage: friendlyError,
            technicalMessage: errorMessage,
        });
    }

    handleSQLError(errorMessage: string): void {
        this.handleError(errorMessage, true);
    }

    private translateSqlError(sqlError: string): string {
        // Only include patterns based on actual observed DuckDB error messages
        // More patterns can be added as we encounter real DuckDB errors
        const errorPatterns: ErrorPattern[] = [
            {
                pattern: /referenced column "([^"]+)" not found/i,
                message: (match: RegExpMatchArray) =>
                    `Column "${match[1]}" was not found in your data. Please check your column names.`,
            },
        ];

        for (const { pattern, message } of errorPatterns) {
            const match = sqlError.match(pattern);
            if (match) return message(match);
        }

        return 'An error occurred while processing your data query.';
    }
}
