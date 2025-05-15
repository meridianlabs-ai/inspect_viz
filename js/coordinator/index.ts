import { AsyncDuckDBConnection } from '@duckdb/duckdb-wasm';

import { MosaicClient, Coordinator } from 'https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.16.2/+esm'



class TableCoordinator {

    private conn_?: AsyncDuckDBConnection;
    private coordinator_?: Coordinator;

    async initialize() {
        const mosaic = await import("https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.16.2/+esm");
        this.coordinator_ = new mosaic.Coordinator();
        this.coordinator_.databaseConnector(mosaic.wasmConnector());
    }

    async addTable(name: string, buffer: Uint8Array) {
        const inserts: Array<Promise<void> | undefined> = []
        inserts.push(this.conn_?.insertArrowFromIPCStream(buffer, { name , create: true }));
        const EOS = new Uint8Array([255,255,255,255,0,0,0,0]);
        inserts.push(this.conn_?.insertArrowFromIPCStream(EOS, { name, create: false }));
        await Promise.all(inserts)
    }

    connectClient(client: MosaicClient) {
        this.coordinator_?.connect(client);
    }
}


// get the global coordinators instance, ensuring we get the same 
// instance eval across different js bundles loaded into the page
const TABLE_COORDINATOR_KEY = Symbol.for('@@table-coordinator')
async function tableCoordinator(): Promise<TableCoordinator> {
    const globalScope: any = typeof window !== 'undefined' ? window : globalThis
    if (!globalScope[TABLE_COORDINATOR_KEY]) {
        console.log("creating coordinator")
        const coordinator = new TableCoordinator()
        await coordinator.initialize()
        globalScope[TABLE_COORDINATOR_KEY] = coordinator;
    }
    return globalScope[TABLE_COORDINATOR_KEY] as TableCoordinator;
}

export async function addTable(name: string, buffer: Uint8Array) {
    console.log("adding table")
    const coordinator = await tableCoordinator();
    await coordinator.addTable(name, buffer);
    console.log("table added")
}


export async function connectClient(client: MosaicClient) {
    const coordinator = await tableCoordinator();
    coordinator.connectClient(client)
}