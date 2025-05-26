import { InputOptions, Input } from './input';

export class Radio extends Input {
    constructor(options: InputOptions) {
        super(options.filterBy, options.element);
        const strongEl = window.document.createElement('strong');
        strongEl.innerText = 'STRONG';
        this.element.appendChild(strongEl);
    }
}
