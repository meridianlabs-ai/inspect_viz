import { Selection } from '@uwdata/mosaic-core';

export class DataFrame {
    constructor(
        public readonly table: string,
        public readonly selection: Selection
    ) {}
}
