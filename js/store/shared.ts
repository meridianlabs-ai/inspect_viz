import { createStore } from 'zustand/vanilla'     
import type { StoreApi } from 'zustand/vanilla'

import type { ColumnTable } from 'arquero'

export interface FrameRecord {
  base:      ColumnTable
  computed:  ColumnTable
}

export interface FrameState {
  frames: Map<string, FrameRecord>

  addDF: (
    id: string,
    base: ColumnTable,
  ) => void
  /* all the mutators you defined earlier … */
}
// ─────────────────────────────────────────────────────

// A symbol guarantees we hit the **same** property even if two
// copies of this file (or different bundle versions) are evaluated.
const STORE_KEY = Symbol.for('@@shared-df-zustand-store')

function initStore(): StoreApi<FrameState> {
  return createStore<FrameState>((set, get) => ({
    frames: new Map(),
    addDF: (id, base) =>
        set(state => {
          const computed = base
          const next     = new Map(state.frames)      // keep immutability
          next.set(id, { base, computed })
          return { frames: next }
        }),
    getDF:  (id: string) => get().frames.get(id)?.computed,
    // …your actions (setFilter, clearFilters, etc.)…
  }))
}


export function addSharedDF(
    id: string,
    table: ColumnTable,
  ) {
    getSharedDFStore().getState().addDF(id, table)
  }

export function getSharedDFStore(): StoreApi<FrameState> {
  const globalScope: any = typeof window !== 'undefined' ? window : globalThis
  if (!globalScope[STORE_KEY]) {
    globalScope[STORE_KEY] = initStore()
  }
  return globalScope[STORE_KEY] as StoreApi<FrameState>
}
