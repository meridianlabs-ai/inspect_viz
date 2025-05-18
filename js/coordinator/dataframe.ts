import { Param, Selection } from '@uwdata/mosaic-core';
import { MosaicQuery } from './query';

export class DataFrame {
    constructor(
        public readonly table: string,
        public readonly queries: MosaicQuery[],
        public readonly params: Map<string, Param>,
        public readonly selection: Selection
    ) {}
}
