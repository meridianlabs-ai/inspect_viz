
import type { ColumnTable } from 'arquero'

export interface FrameRecord {
  base:      ColumnTable
  computed:  ColumnTable
}

export interface FrameState {
  addDF: (
    id: string,
    base: ColumnTable,
  ) => void
  getDF: (id: string) => FrameRecord | undefined
}
// ─────────────────────────────────────────────────────


export function addSharedDF(
    id: string,
    table: ColumnTable,
) {
  getSharedDFStore().addDF(id, table)
}

export function getSharedDF(id: string): FrameRecord | undefined {
  return getSharedDFStore().getDF(id)
}

function getSharedDFStore(): FrameState {
  const globalScope: any = typeof window !== 'undefined' ? window : globalThis
  if (!globalScope[STORE_KEY]) {
    globalScope[STORE_KEY] = initStore()
  }
  return globalScope[STORE_KEY] as FrameState
}


// A symbol guarantees we hit the **same** property even if two
// copies of this file (or different bundle versions) are evaluated.
const STORE_KEY = Symbol.for('@@shared-df-zustand-store')

  function initStore(): FrameState {
    
    const frames = new Map<string, FrameRecord>();
  
    return {
      addDF: (id, base ) => {
        frames.set(id, { base, computed: base });
      },
      getDF: (id) => {
        return frames.get(id)
      },
    }
  }
  