import React from 'react'
import ReactDOM from 'react-dom/client'
import { ClerkProvider } from '@clerk/clerk-react'
import { BrowserRouter } from 'react-router-dom'
import App from './App.jsx'
import './index.css'

const PUBLISHABLE_KEY = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY

if (!PUBLISHABLE_KEY) {
    throw new Error('Missing Publishable Key')
}

ReactDOM.createRoot(document.getElementById('root')).render(
    <React.StrictMode>
        <ClerkProvider
            publishableKey={PUBLISHABLE_KEY}
            appearance={{
                layout: {
                    socialButtonsVariant: 'iconButton',
                    socialButtonsPlacement: 'bottom'
                },
                variables: {
                    colorPrimary: '#B8FF00',
                    colorBackground: '#0a0a0a',
                    colorInputBackground: '#1a1a1a',
                    colorInputText: '#ffffff',
                    colorText: '#ffffff',
                    colorTextSecondary: 'rgba(255, 255, 255, 0.6)',
                    borderRadius: '0.75rem'
                },
                elements: {
                    formButtonPrimary:
                        'bg-accent hover:bg-accent/90 text-black font-semibold shadow-[0_0_15px_rgba(184,255,0,0.3)]',
                    card: 'bg-dark-900 border border-white/10',
                    headerTitle: 'text-white font-bold',
                    headerSubtitle: 'text-white/60',
                    socialButtonsBlockButton:
                        'bg-white/5 hover:bg-white/10 border border-white/10 text-white/80',
                    formFieldInput:
                        'bg-white/5 border-white/10 text-white focus:border-accent',
                    footerActionLink: 'text-accent hover:text-accent/80'
                }
            }}
        >
            <BrowserRouter>
                <App />
            </BrowserRouter>
        </ClerkProvider>
    </React.StrictMode>,
)
