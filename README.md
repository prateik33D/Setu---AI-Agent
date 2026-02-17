# SETU - AI Agent Platform

SETU (सेतु) is a powerful AI agent platform that bridges your digital world by automating tasks across multiple services like Gmail, Google Calendar, Notion, GitHub, and more.

## Features

- **Multi-Service Integration**: Connect Gmail, Google Calendar, Google Meet, Google Drive, Google Sheets, Google Docs, Notion, GitHub, and Slack
- **AI-Powered Task Automation**: Natural language task processing using Groq/OpenAI
- **Beautiful UI**: Modern, responsive landing page with integration panel UX
- **OAuth Authentication**: Secure token storage with encryption
- **Real-time Task Execution**: Live progress tracking and result display
- **Clerk Authentication**: User authentication handled by Clerk

## Prerequisites

- Node.js (v18+)
- Python (v3.9+)
- Git
- API Keys:
  - Groq API Key (free tier available)
  - Google OAuth credentials
  - Notion OAuth credentials (optional)
  - GitHub OAuth credentials (optional)
  - Clerk authentication keys

## Installation

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
```

### Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env
# Edit .env with your Clerk keys
```

## Configuration

### Backend `.env` File

```env
# Encryption key (generate with: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")
ENCRYPTION_KEY=your-generated-fernet-key-here

# LLM (at least one required)
GROQ_API_KEY=your-groq-api-key-here
OPENAI_API_KEY=your-openai-key-optional

# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-secret
GOOGLE_REDIRECT_URI=http://localhost:8000/api/v1/auth/google/callback

# Notion
NOTION_CLIENT_ID=your-notion-client-id
NOTION_CLIENT_SECRET=your-notion-secret
NOTION_REDIRECT_URI=http://localhost:8000/api/v1/auth/notion/callback

# GitHub
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-secret

# Clerk
CLERK_SECRET_KEY=your-clerk-secret-key
```

### Frontend `.env` File

```env
VITE_CLERK_PUBLISHABLE_KEY=your-clerk-publishable-key
VITE_API_URL=http://localhost:8000
```

## Running the Application

### Start Backend

```bash
cd backend
uvicorn app.main:app --reload
```

Backend will run on `http://localhost:8000`

### Start Frontend

```bash
cd frontend
npm run dev
```

Frontend will run on `http://localhost:5173`

## Usage

1. **Sign Up/Login**: Use Clerk authentication to create an account
2. **Connect Integrations**: Click on any service icon to connect via OAuth
3. **Create Tasks**: Type natural language tasks like:
   - "Send email to john@test.com about meeting tomorrow"
   - "Set reminder Feb 20 at 2pm for team meeting"
   - "Create Notion page for Q1 planning"
4. **View Results**: See real-time progress and results in the integration panel

## Architecture

```
Frontend (React + Vite + Tailwind)
    ↓
Backend (FastAPI + SQLAlchemy)
    ↓
AI Orchestrator (Groq/OpenAI)
    ↓
Service Integrations (Google, Notion, GitHub, Slack)
```

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── agents/          # AI agent orchestrator
│   │   ├── api/             # API endpoints
│   │   ├── core/            # Database, config
│   │   ├── models/          # Data models
│   │   └── services/       # Service integrations
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── services/        # API service
│   │   └── SetuLandingPage.jsx
│   └── package.json
└── README.md
```

## Security

- OAuth tokens are encrypted using Fernet symmetric encryption
- Tokens stored securely in SQLite database
- Clerk handles all user authentication
- Environment variables for sensitive data

## Testing

```bash
cd backend
pytest
```

## License

This project is open source and available for educational purposes.


## Acknowledgments

- Built with FastAPI, React, and modern web technologies
- Uses Groq for free AI processing
- Clerk for authentication

---

**SETU** - Bridge of your digital world 🌉
