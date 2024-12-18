"use client";

import { Provider as RawProvider } from "react-redux";

import { store } from "./store";

export function Provider({ children }: { children: React.ReactNode }) {
    return <RawProvider store={store}>{children}</RawProvider>;
}