import {
    coordinator,
    MosaicClient,
    Selection,
} from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.16.2/+esm';

export interface InputOptions {
    element: HTMLElement;
    filterBy: Selection;
}

export type InputFunction = (options: InputOptions) => HTMLElement;

export function input<T extends new (...args: any[]) => Input>(
    InputClass: T,
    ...params: ConstructorParameters<T>
): HTMLElement {
    const input = new InputClass(...params);
    coordinator().connect(input);
    return input.element;
}

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
