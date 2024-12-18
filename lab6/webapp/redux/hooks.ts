import type { TypedUseSelectorHook } from 'react-redux';

import { useDispatch as useRawDispatch, useSelector as useRawSelector } from 'react-redux';

import type { AppDispatch, RootState } from './store';

export const useDispatch: () => AppDispatch = useRawDispatch;
export const useSelector: TypedUseSelectorHook<RootState> = useRawSelector;