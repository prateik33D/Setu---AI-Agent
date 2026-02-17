import { useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'

export default function OAuthCallback() {
    const navigate = useNavigate()
    const [searchParams] = useSearchParams()

    useEffect(() => {
        const token = searchParams.get('token')
        const error = searchParams.get('error')

        if (error) {
            console.error('OAuth error:', error)
            navigate('/?error=oauth_failed')
            return
        }

        if (token) {
            navigate('/?success=integration_connected')
        } else {
            navigate('/')
        }
    }, [searchParams, navigate])

    return (
        <div className="min-h-screen bg-dark-900 flex items-center justify-center">
            <div className="text-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-accent mx-auto mb-4"></div>
                <p className="text-white/60">Completing authentication...</p>
            </div>
        </div>
    )
}
