import {
    MosaicClient,
    Selection,
} from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.16.2/+esm';

export interface InputOptions {
    element: HTMLElement;
    filterBy: Selection;
}

export type InputFunction = (options: InputOptions) => HTMLElement;

// from unexported Input class in mosaic-inputs
export class Input extends MosaicClient {
    public readonly element: HTMLElement;
    constructor(filterBy: Selection, element: HTMLElement, className: string = 'input') {
        super(filterBy);
        this.element = element || document.createElement('div');
        if (className) this.element.setAttribute('class', className);
        Object.defineProperty(this.element, 'value', { value: this });
    }

    activate() {
        // subclasses should override
    }
}
