import type { Metadata } from "next";

import { Launcher } from "@/components/Common";
import Script from 'next/script';

import { Providers } from "./providers";
import './globals.css';

// interface Metadata extends RawMetadata {
//   'application-name': string;
// }

export const metadata: Metadata = {
  description: 'DD round bot',
  // manifest: '/manifest.json',
  title: 'DD round bot'
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return <html lang='en'>
    <body>
      <Providers>
        <Script src="https://telegram.org/js/telegram-web-app.js?1" />
        <Launcher />

        <main style={{ alignItems: 'center', display: 'flex', flexDirection: 'column', justifyContent: 'center', width: '100%', color: 'black' }}>
          {children}
        </main>
      </Providers>
    </body>
  </html>
}
