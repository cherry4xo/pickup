'use client';
import { ChakraProvider, extendTheme } from '@chakra-ui/react';
import { CacheProvider } from '@chakra-ui/next-js';
import { Provider } from "@/redux/provider";
import '@fontsource-variable/manrope';
import '@fontsource-variable/montserrat';

export function Providers({ children }: { children: React.ReactNode }) {
    return <Provider>
        <CacheProvider>
            <ChakraProvider theme={extendTheme({
                colors: {
                    main: {
                        100: '#000000'
                    }
                }
            })}>
                {children}
            </ChakraProvider>
        </CacheProvider>
    </Provider>
}