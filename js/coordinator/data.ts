import { Selection } from '@uwdata/mosaic-core';

export class Data {
    constructor(
        public readonly table: string,
        public readonly selection: Selection
    ) {}
}
