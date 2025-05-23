import { AsyncDuckDBConnection } from 'https://cdn.jsdelivr.net/npm/@duckdb/duckdb-wasm@1.29.0/+esm';

import {
    MosaicClient,
    wasmConnector,
    Param,
} from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.16.2/+esm';

import {
    InstantiateContext,
    parseSpec,
} from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-spec@0.16.2/+esm';

import { initDuckdb } from './duckdb';
import { sleep } from '../util/wait';

class VizCoordinator {
    private readonly ctx_: InstantiateContext;
    private readonly tables_ = new Set<string>();

    constructor(private readonly conn_: AsyncDuckDBConnection) {
        this.ctx_ = new InstantiateContext();
        this.ctx_.coordinator.databaseConnector(wasmConnector({ connection: this.conn_ }));
    }

    addParams(params: Record<string, unknown>) {
        const spec = { params: params, hspace: 10 } as any;
        const ast = parseSpec(spec);
        for (const [name, node] of Object.entries(ast.params)) {
            if (!this.ctx_.activeParams.has(name)) {
                const param = (node as any).instantiate(this.ctx_);
                this.ctx_.activeParams.set(name, param);
            }
        }
    }

    getParams() {
        return this.ctx_.activeParams;
    }

    getParam(name: string): Param | undefined {
        return this.ctx_.activeParams.get(name);
    }

    async addData(id: string, buffer: Uint8Array) {
        // insert table into database
        await this.conn_?.insertArrowFromIPCStream(buffer, {
            name: id,
            create: true,
        });

        // add to list of tables
        this.tables_.add(id);
    }

    async waitForData(id: string) {
        // at startup we can't control the order of df producing and df consuming
        // widgets, so we may need to wait and retry for the data frame
        while (true) {
            if (this.tables_.has(id)) {
                return;
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
