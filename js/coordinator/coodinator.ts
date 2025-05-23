import { AsyncDuckDBConnection } from 'https://cdn.jsdelivr.net/npm/@duckdb/duckdb-wasm@1.29.0/+esm';

import {
    MosaicClient,
    wasmConnector,
    Selection,
    Param,
} from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.16.2/+esm';

import { InstantiateContext } from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-spec@0.16.2/+esm';

import { initDuckdb } from './duckdb';
import { DataFrame } from './dataframe';
import { sleep } from '../util/wait';
import { ParamDef } from './param';

class VizCoordinator {
    private readonly ctx_: InstantiateContext;
    private readonly dfs_ = new Map<string, DataFrame>();

    constructor(private readonly conn_: AsyncDuckDBConnection) {
        this.ctx_ = new InstantiateContext();
        this.ctx_.coordinator.databaseConnector(wasmConnector({ connection: this.conn_ }));
    }

    addParams(params: ParamDef[]) {
        for (const param of params) {
            this.addParam(param.id, param.default);
        }
    }

    getParams() {
        return this.ctx_.activeParams;
    }

    addParam(name: string, value: number | boolean | string): Param {
        if (!this.ctx_.activeParams.has(name)) {
            this.ctx_.activeParams.set(name, Param.value(value));
        }
        return this.ctx_.activeParams.get(name)!;
    }

    getParam(name: string): Param | undefined {
        return this.ctx_.activeParams.get(name);
    }

    async addDataFrame(id: string, buffer: Uint8Array) {
        // insert table into database
        await this.conn_?.insertArrowFromIPCStream(buffer, {
            name: id,
            create: true,
        });

        // create and register df
        const df = new DataFrame(id, Selection.intersect());
        this.dfs_.set(id, df);
    }

    async getDataFrame(id: string) {
        // at startup we can't control the order of df producing and df consuming
        // widgets, so we may need to wait and retry for the data frame
        while (true) {
            const df = this.dfs_.get(id);
            if (df) {
                return df;
            } else {
                await sleep(100);
            }
        }
    }

    getInstantiateContext(): InstantiateContext {
        return this.ctx_;
    }

    async connectClient(client: MosaicClient) {
        this.ctx_.coordinator.connect(client);
    }
}

// get the global coordinators instance, ensuring we get the same
// instance eval across different js bundles loaded into the page
const VIZ_COORDINATOR_KEY = Symbol.for('@@inspect-viz-coordinator');
async function vizCoordinator(): Promise<VizCoordinator> {
    const globalScope: any = typeof window !== 'undefined' ? window : globalThis;
    if (!globalScope[VIZ_COORDINATOR_KEY]) {
        globalScope[VIZ_COORDINATOR_KEY] = (async () => {
            const duckdb = await initDuckdb();
            const conn = await duckdb.connect();
            return new VizCoordinator(conn);
        })();
    }
    return globalScope[VIZ_COORDINATOR_KEY] as Promise<VizCoordinator>;
}

export { VizCoordinator, vizCoordinator };
