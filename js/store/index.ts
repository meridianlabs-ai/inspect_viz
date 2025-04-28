

import { useStore } from 'zustand'
import { useShallow }  from 'zustand/shallow'
import { getSharedDFStore, addSharedDF } from './shared'

const store = getSharedDFStore()

export { addSharedDF }

export function useSharedDF(id: string) {
  return useStore(
    store,
    useShallow((s) => ({
      df: s.frames.get(id)?.computed
    })),
  )
}