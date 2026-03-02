# 📊 Compliance Audit & Agent Performance Dashboard

A state-of-the-art, AI-powered system designed for quality assurance, compliance monitoring, and automated agent coaching. This platform analyzes both **Audio Conversations** and **Email Interactions** to provide actionable insights for customer service teams.

---

## 🚀 Key Features

### 🎙️ AI Audio Auditing
- **Instant Transcription**: Powered by **Groq Whisper API** (whisper-large-v3), reducing transcription time from minutes to seconds.
- **Smart Diarization**: Automatically labels 'Agent' vs 'Customer' dialogue using advanced LLM reasoning.
- **Chunk-wise Scoring**: Detailed analysis of empathy and professionalism throughout the entire conversation.

### 📧 Stealth Email Analysis
- **Secure Browser Sync**: Uses **Playwright with Stealth Mode** to safely extract email content while bypassing "insecure browser" blocks.
- **Persistent Sessions**: Saves your login state locally in `data/user_data`, so you only need to sign in to Gmail once.
- **Multimodal Compliance**: Applies the same rigorous policy checks used for audio directly to agent emails.

### 🎯 Advanced Analytics & Coaching
- **Leaderboard**: Maps agents on a 2D performance matrix: *Stars (High E / High P)*, *Robots*, *Charmers*, and *Risks*.
- **AI Coaching Roadmap**: Automatically clusters team-wide mistakes and generates a personalized training plan using Groq Llama-3.
- **RAG-Powered Compliance**: Uses a Vector DB (Pinecone) to retrieve relevant company policies for every single audit.

---

## 🛠️ Technology Stack

- **Frontend**: Streamlit (Advanced Dark Mode UI)
- **AI Core**: Groq Cloud (Llama-3 & Whisper-v3)
- **Vector DB**: Pinecone (Compliance Policy RAG)
- **Automation**: Playwright (with Stealth & Persistent Context)
- **Analysis**: Pandas & Plotly (Real-time data visualization)

---

## ⚙️ Installation & Setup

### 1. Requirements
Ensure you have **Python 3.10+** installed.

```bash
# Install dependencies
pip install -r requirements.txt

# Setup Playwright browsers
playwright install chromium
```

### 2. Configure Environment
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=gsk_your_key_here
PINECONE_API_KEY=pcsk_your_key_here
```

### 3. Initialize Policies (Optional)
Upload your company policies from `data/policy.txt` to Pinecone:
```bash
python backend/upload_policies.py
```

---

## 🖥️ Usage Guide

### Launching the Dashboard
```bash
streamlit run frontend/dashboard.py
```

### Audio Audit Workflow
1. Enter the Agent's Name in the sidebar.
2. Upload an **MP3** file.
3. Click "Process & Analyze". The system will transcribe (via Groq), label speakers, and score.
4. Results appear instantly on the **Home** and **Reports** pages.

### Email Audit Workflow
1. Navigate to the **Email Analysis** page.
2. Click "Launch Email Browser" to log in to Gmail.
3. Click "Extract & Score from Browser" while viewing an email.
4. The system will securely "scrape" the email and run a full compliance audit.

---

## 📂 Project Structure

- `frontend/`: Streamlit UI and dashboard logic.
- `backend/`: Core AI logic (transcription, scoring, stealth extraction).
- `data/`: Local storage for policies and transient data (session-safe).
- `requirements.txt`: Project dependencies including `playwright-stealth` and `groq`.

---

## 🔒 Privacy & Security
- **Email Sessions**: Login data is stored locally in `data/user_data/` and is purposefully excluded from Git tracking via `.gitignore`.
- **API Security**: Keys are managed through `.env` and never hardcoded in the repository.

---
*Built with ❤️ for High-Performance Quality Assurance.*
