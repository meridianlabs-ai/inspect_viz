
import { Table } from 'arquero';
import { Data } from 'plotly.js-dist-min';

export function bindTable(traces: Data[], table: Table): Data[] {

    // don't mutate the passed traces
    traces = structuredClone(traces);

    // table columns as arrays
    const columns = columnData(table)

    // handle each trace
    traces.forEach((trace: Data) => {
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

  type ColArray = ArrayLike<unknown>; 

  function columnData(table: Table): Record<string, ColArray> {
    const data: Record<string, ColArray> = {};
    for (const name of table.columnNames()) { 
      data[name] = table.array(name) 
    }
    return data;
  }

  function columnMapping(trace: Data, cols: string[]): Record<string,string>  {
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
  
    if (!map.x && !map.y && cols.length >= 2) {
      map.x = cols[0]; map.y = cols[1];
      if (['scatter3d','surface','mesh3d'].includes(trace.type ?? '')
          && cols.length >= 3) map.z = cols[2];
    }
    return map;
  }

  function setData(trace: Data, path: string[], val: unknown) {
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
      Array.isArray(v)
        ? [`${prefix}${k}`]
        : typeof v === 'object' && v !== null
          ? arrayProps(v, `${prefix}${k}.`)
          : []
    );
  }