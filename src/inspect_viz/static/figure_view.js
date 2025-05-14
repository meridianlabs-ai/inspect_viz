// js/store/shared.ts
function getSharedDF(id) {
  return getSharedDFStore().getDF(id);
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

// js/util/binding.ts
function bindTable(traces, table) {
  traces = structuredClone(traces);
  const columns = columnData(table);
  traces.forEach((trace) => {
    const mapping = columnMapping(trace, Object.keys(columns));
    for (const [attr, col] of Object.entries(mapping)) {
      const arr = columns[col];
      if (arr) {
        setData(trace, attr.split("."), arr);
      } else {
        console.warn(`Column "${col}" not found in table`);
      }
    }
  });
  return traces;
}
function columnData(table) {
  const data = {};
  for (const name of table.columnNames()) {
    data[name] = table.array(name);
  }
  return data;
}
function columnMapping(trace, cols) {
  const map = {};
  const lc = cols.map((c) => c.toLowerCase());
  for (const p of arrayProps(trace)) {
    const simple = p.split(".").pop().toLowerCase();
    const i2 = lc.indexOf(simple);
    if (i2 === -1) continue;
    const exists = p.split(".").reduce((o, k) => o?.[k], trace) !== void 0;
    if (exists) map[p] = cols[i2];
  }
  const used = new Set(Object.values(map));
  const unused = cols.filter((c) => !used.has(c));
  let i = 0;
  const needsX = !map.x && (!isOrientable(trace) || trace.orientation !== "h");
  const needsY = !map.y && (isOrientable(trace) && trace.orientation === "h" ? false : true);
  if (needsX && unused[i]) {
    map.x = unused[i++];
  }
  if (needsY && unused[i]) {
    map.y = unused[i++];
  }
  const is3d = ["scatter3d", "surface", "mesh3d"].includes(trace.type ?? "");
  if (is3d && !map.z && unused[i]) {
    map.z = unused[i++];
  }
  return map;
}
function setData(trace, path, val) {
  const last = path.pop();
  let cur = trace;
  for (const k of path) {
    if (cur[k] == null || typeof cur[k] !== "object") cur[k] = {};
    cur = cur[k];
  }
  cur[last] = val;
}
function arrayProps(obj, prefix = "") {
  return Object.entries(obj).flatMap(
    ([k, v]) => Array.isArray(v) || ArrayBuffer.isView(v) ? [`${prefix}${k}`] : typeof v === "object" && v !== null ? arrayProps(v, `${prefix}${k}.`) : []
  );
}
function isOrientable(t) {
  return "orientation" in t;
}

// js/figure_view.ts
var Plotly = (await import("https://esm.sh/plotly.js-dist-min@3.0.1")).default;
function render({ model, el }) {
  const df_id = model.get("df_id");
  const figure_json = model.get("figure_json");
  const figure = JSON.parse(figure_json);
  setTimeout(() => {
    const df = getSharedDF(df_id);
    if (df) {
      const data = bindTable(figure.data, df.computed);
      Plotly.react(el, data, figure.layout, figure.config || {});
    }
  }, 1e3);
}
var figure_view_default = { render };
export {
  figure_view_default as default
};
