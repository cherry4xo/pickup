'use client';
import { motion } from 'framer-motion';
import { ease } from "@/utils/misc";

export function Launcher() {
    return <>
        <motion.div
            initial={{ opacity: 1 }}
            animate={{ opacity: 0 }}
            transition={{ duration: 0.3, ease }}
            style={{ width: '100vw', height: '100vh', position: 'fixed', top: 0, left: 0, zIndex: 10000, background: 'black', pointerEvents: 'none' }}
        />
    </>
}