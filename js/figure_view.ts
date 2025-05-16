import type { RenderProps } from '@anywidget/types';

import {
    MosaicClient,
    toDataColumns,
} from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.16.2/+esm';
import { Query } from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-sql@0.16.2/+esm';

import { connectClient } from './coordinator';

import Plotly from 'https://esm.sh/plotly.js-dist-min@3.0.1';

import './figure_view.css';
import { bindTable } from './util/binding';

interface FigureRecord {
    table: string;
    figure_json: string;
}

class FigureView extends MosaicClient {
    constructor(
        private readonly table_: string,
        private readonly figure_: any,
        private readonly el_: HTMLElement
    ) {
        super();
    }

    query(_filter?: any): any {
        return Query.select('*').from(this.table_);
    }

    queryResult(data: any) {
        const columns = toDataColumns(data).columns as Record<string, ArrayLike<unknown>>;
        const table = bindTable(this.figure_.data, columns);
        Plotly.react(this.el_, table, this.figure_.layout, this.figure_.config || {});
        return this;
    }
}

export async function render({ model, el }: RenderProps<FigureRecord>) {
    const table: string = model.get('table');
    const figure_json: string = model.get('figure_json');
    const figure = JSON.parse(figure_json);

    const view = new FigureView(table, figure, el);

    await connectClient(table, view);
}
