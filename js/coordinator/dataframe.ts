import { Param, Selection } from '@uwdata/mosaic-core';
import { SelectQuery } from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-sql@0.16.2/+esm';

export class DataFrame {
    constructor(
        public readonly table: string,
        public readonly selection: Selection,
        public readonly queries: SelectQuery[],
        public readonly params: Map<string, Param>
    ) {}
}
