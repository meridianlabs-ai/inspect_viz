// js/coordinator/index.ts
var TableCoordinator = class {
  async initialize() {
    const mosaic = await import("https://cdn.jsdelivr.net/npm/@uwdata/mosaic-core@0.16.2/+esm");
    this.coordinator_ = new mosaic.Coordinator();
    this.coordinator_.databaseConnector(mosaic.wasmConnector());
  }
  async addTable(name, buffer) {
    const inserts = [];
    inserts.push(this.conn_?.insertArrowFromIPCStream(buffer, { name, create: true }));
    const EOS = new Uint8Array([255, 255, 255, 255, 0, 0, 0, 0]);
    inserts.push(this.conn_?.insertArrowFromIPCStream(EOS, { name, create: false }));
    await Promise.all(inserts);
  }
  connectClient(client) {
    this.coordinator_?.connect(client);
  }
};
var TABLE_COORDINATOR_KEY = Symbol.for("@@table-coordinator");
async function tableCoordinator() {
  const globalScope = typeof window !== "undefined" ? window : globalThis;
  if (!globalScope[TABLE_COORDINATOR_KEY]) {
    console.log("creating coordinator");
    const coordinator = new TableCoordinator();
    await coordinator.initialize();
    globalScope[TABLE_COORDINATOR_KEY] = coordinator;
  }
  return globalScope[TABLE_COORDINATOR_KEY];
}
async function addTable(name, buffer) {
  console.log("adding table");
  const coordinator = await tableCoordinator();
  await coordinator.addTable(name, buffer);
  console.log("table added");
}

// js/shared_df.ts
async function render({ model }) {
  const id = model.get("id");
  const buffer = model.get("buffer");
  const arrowBuffer = new Uint8Array(buffer.buffer, buffer.byteOffset, buffer.byteLength);
  await addTable(id, arrowBuffer);
}
var shared_df_default = { render };
export {
  shared_df_default as default
};
