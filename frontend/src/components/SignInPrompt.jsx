import { SignInButton, SignUpButton } from '@clerk/clerk-react'

const SignInPrompt = ({ show, onClose }) => {
    if (!show) return null

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm">
            <div className="bg-dark-900 border border-white/10 rounded-2xl p-8 max-w-md mx-4">
                <h2 className="text-2xl font-bold text-white mb-4">Sign in to continue</h2>
                <p className="text-white/60 mb-6">
                    Create an account or sign in to start automating your workflows with AI agents.
                </p>
                <div className="flex gap-3">
                    <SignUpButton mode="modal">
                        <button className="flex-1 bg-accent text-black font-semibold px-6 py-3 rounded-lg hover:bg-accent/90 transition-all">
                            Get Started
                        </button>
                    </SignUpButton>
                    <SignInButton mode="modal">
                        <button className="flex-1 bg-white/5 text-white font-medium px-6 py-3 rounded-lg hover:bg-white/10 transition-all border border-white/10">
                            Sign In
                        </button>
                    </SignInButton>
                </div>
                <button
                    onClick={onClose}
                    className="mt-4 text-white/40 hover:text-white/60 text-sm w-full"
                >
                    Close
                </button>
            </div>
        </div>
    )
}

export default SignInPrompt
