import { Routes, Route } from 'react-router-dom'
import SetuLandingPage from './SetuLandingPage'
import OAuthCallback from './components/OAuthCallback'
import './index.css'

function App() {
    return (
        <Routes>
            <Route path="/" element={<SetuLandingPage />} />
            <Route path="/oauth-callback" element={<OAuthCallback />} />
        </Routes>
    )
}

export default App
