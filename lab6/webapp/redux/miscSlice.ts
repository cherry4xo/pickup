import type { PayloadAction } from "@reduxjs/toolkit";

import { createSlice } from '@reduxjs/toolkit';

interface MiscState {
}

const initialState: MiscState = {
};

export const miscSlice = createSlice({
    name: 'misc',
    initialState,
    reducers: {
    }
})

export const { } = miscSlice.actions;
export default miscSlice.reducer;