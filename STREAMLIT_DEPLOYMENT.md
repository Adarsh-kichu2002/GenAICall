# Streamlit Cloud Deployment Guide

## Prerequisites
- GitHub account
- Streamlit Cloud account (free tier available at https://streamlit.io/cloud)
- Your repository pushed to GitHub

## Deployment Steps

### 1. Push to GitHub
```bash
git add .
git commit -m "Prepare for Streamlit Cloud deployment"
git push origin main
```

### 2. Create Streamlit Cloud App
1. Go to https://share.streamlit.io
2. Click "New app"
3. Select your GitHub repository
4. Select the branch (main)
5. Set the main file path to: `frontend/dashboard.py`
6. Click "Deploy"

### 3. Add Secrets
1. In Streamlit Cloud app dashboard, click on "Settings" (gear icon)
2. Go to "Secrets" tab
3. Add your secrets in TOML format:
```toml
GROQ_API_KEY = "your-groq-api-key"
PINECONE_API_KEY = "your-pinecone-api-key" 
PINECONE_ENVIRONMENT = "your-pinecone-environment"
```
4. Save

### 4. Configure Data Location
The app expects data files in the `data/` directory. Make sure to:
- Include data files in your GitHub repository, OR
- Modify the app to fetch data from a cloud storage service (S3, Azure Blob, etc.)

## Notes
- The app runs `backend/scoring_engine.py` on startup to generate `audit_results.csv`
- Make sure all required data files are available (3_labeled_dialogue.txt, policy.txt)
- API keys are stored securely in Streamlit Cloud and never exposed

## Troubleshooting
- If seeing "audit_results.csv not found", ensure `backend/scoring_engine.py` runs successfully
- Check app logs in Streamlit Cloud dashboard for detailed error messages
- Verify all dependencies in `requirements.txt` are compatible
