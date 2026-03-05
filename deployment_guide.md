# Streamlit Cloud Deployment Guide

Follow these steps to deploy your **GenerativeAI Customer Support Quality Auditor** to Streamlit Cloud.

## 1. Prerequisites
- Your code must be pushed to a public or private GitHub repository (Done: [GenerativeAI-Customer-Support-Quality-Auditor](https://github.com/Akshayaa1010/GenerativeAI-Customer-Support-Quality-Auditor)).
- A [Streamlit Cloud](https://share.streamlit.io/) account connected to your GitHub.

## 2. Deployment Steps
1. Log in to **Streamlit Cloud**.
2. Click **"New app"**.
3. Select your repository: `Akshayaa1010/GenerativeAI-Customer-Support-Quality-Auditor`.
4. Set the **Main file path** to: `frontend/dashboard.py`.
5. Click **"Deploy!"**.

## 3. Critical Configuration (Secrets)
Standard `.env` files do **not** work on Streamlit Cloud. You must add your API keys to the Streamlit Secrets manager:

1. In your Streamlit app dashboard, go to **Settings** > **Secrets**.
2. Paste the following (replacing with your actual keys):

```toml
GROQ_API_KEY = "your_groq_api_key_here"
PINECONE_API_KEY = "your_pinecone_api_key_here"
```

## 4. Playwright Browser Support
Streamlit Cloud handles `requirements.txt` and `packages.txt` automatically. I have added a `setup.sh` that will attempt to install the Chromium browser binaries on the server.

## 5. Persistent Storage Warning
Streamlit Cloud uses a **rebootable file system**. 
- `audit_results.csv` and `user_data` will be **wiped** every time the app reboots or you push new code.
- **Solution**: For a production-ready app, you should eventually connect a database (like Supabase or Firestore). For initial testing, the current setup will work but data won't persist forever.
