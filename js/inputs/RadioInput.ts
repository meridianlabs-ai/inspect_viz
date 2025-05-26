import { coordinator } from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.16.2/+esm';

import { InputOptions, Input } from './types';

class RadioInput extends Input {
    constructor(options: InputOptions) {
        super(options.filterBy, options.element);
        const strongEl = window.document.createElement('strong');
        strongEl.innerText = 'STRONG';
        this.element.appendChild(strongEl);
    }
}

export function radio(options: InputOptions): HTMLElement {
    const input = new RadioInput(options);
    coordinator().connect(input);
    return input.element;
}
