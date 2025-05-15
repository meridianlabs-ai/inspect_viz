
import * as Plotly from 'plotly.js';



export function bindTable(traces: Plotly.Data[], columns: Record<string,ArrayLike<unknown>>): Plotly.Data[] {

    // don't mutate the passed traces
    traces = structuredClone(traces);


    // handle each trace
    traces.forEach((trace: Plotly.Data) => {
      // map the columns
      const mapping = columnMapping(trace, Object.keys(columns))

      // apply the data from the arquero table
      for (const [attr, col] of Object.entries(mapping)) {
        const arr = columns[col];
        if (arr) {
          setData(trace, attr.split('.'), arr);
        } else {
          console.warn(`Column "${col}" not found in table`);
        } 
      }
    })

    // return traces
    return traces

  }

 
  function columnMapping(trace: Plotly.Data, cols: string[]): Record<string,string>  {
    const map:  Record<string,string> = {};
    const lc = cols.map(c => c.toLowerCase());
  
    for (const p of arrayProps(trace) ) {
      const simple = p.split('.').pop()!.toLowerCase();
      const i = lc.indexOf(simple);
      if (i === -1) continue;
  
      const exists = p.split('.').reduce<unknown>((o,k)=>(o as any)?.[k], trace)
                       !== undefined;
      if (exists) map[p] = cols[i];
    }
  
    // discover required bindings
    const used   = new Set(Object.values(map));
    const unused = cols.filter(c => !used.has(c));
    let i = 0;
    const needsX = !map.x && (!isOrientable(trace) || trace.orientation !== 'h');
    const needsY = !map.y && (isOrientable(trace) && trace.orientation === 'h' ? false : true);

    // fill x
    if (needsX && unused[i]) {
      map.x = unused[i++];
    }

    // fill y
    if (needsY && unused[i]) {
      map.y = unused[i++];
    }

    // optional z for 3-D traces
    const is3d = ['scatter3d', 'surface', 'mesh3d'].includes(trace.type ?? '');
    if (is3d && !map.z && unused[i]) {
      map.z = unused[i++];
    }

    return map;
  }

  function setData(trace: Plotly.Data, path: string[], val: unknown) {
    const last = path.pop()!;
    let cur = trace as Record<string,unknown>;
    for (const k of path) {
      if (cur[k] == null || typeof cur[k] !== 'object') cur[k] = {};
      cur = cur[k] as Record<string, unknown>;
    }
    cur[last] = val;
  }

  function arrayProps(obj: any, prefix = ''): string[] {
    return Object.entries(obj).flatMap(([k, v]) =>
      Array.isArray(v) || ArrayBuffer.isView(v)
        ? [`${prefix}${k}`]
        : typeof v === 'object' && v !== null
          ? arrayProps(v, `${prefix}${k}.`)
          : []
    );
  }

  interface OrientableTrace {
    orientation?: 'h' | 'v';
  }
  
  function isOrientable(t: Plotly.Data): t is Plotly.Data & OrientableTrace {
    return 'orientation' in t;
  }