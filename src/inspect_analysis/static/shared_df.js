// js/store/shared.ts
function addSharedDF(id, table) {
  getSharedDFStore().addDF(id, table);
}
function getSharedDFStore() {
  const globalScope = typeof window !== "undefined" ? window : globalThis;
  if (!globalScope[STORE_KEY]) {
    globalScope[STORE_KEY] = initStore();
  }
  return globalScope[STORE_KEY];
}
var STORE_KEY = Symbol.for("@@shared-df-zustand-store");
function initStore() {
  const frames = /* @__PURE__ */ new Map();
  return {
    addDF: (id, base) => {
      frames.set(id, { base, computed: base });
    },
    getDF: (id) => {
      return frames.get(id);
    }
  };
}

// js/shared_df.ts
var aq = await import("https://cdn.jsdelivr.net/npm/arquero@8.0.1/+esm");
function render({ model }) {
  const id = model.get("id");
  const buffer = model.get("buffer");
  const df = aq.fromArrow(
    new Uint8Array(buffer.buffer, buffer.byteOffset, buffer.byteLength)
  );
  addSharedDF(id, df);
}
var shared_df_default = { render };
export {
  shared_df_default as default
};
