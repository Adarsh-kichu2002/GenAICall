# Streamlit Cloud Deployment Checklist

## Pre-Deployment Setup ✅

Your project has been prepared for Streamlit Cloud deployment with the following:

### Files Created/Updated:
- ✅ `.streamlit/config.toml` - Streamlit configuration (theme, client settings)
- ✅ `.streamlit/secrets.toml.example` - Template for required API keys
- ✅ `frontend/dashboard.py` - Updated with proper path handling and auto-initialization
- ✅ `backend/scoring_engine.py` - Fixed file path issues
- ✅ `requirements.txt` - All dependencies listed

### Key Improvements:
- Auto-initialization: Dashboard now automatically runs scoring_engine.py if audit_results.csv is missing
- Proper path handling: All file paths use absolute paths based on project root
- Environment variable support: Ready to use Streamlit secrets for API keys

---

## Deployment Steps

### Step 1: Push to GitHub
```bash
# From your project root directory
git add .
git commit -m "Prepare for Streamlit Cloud deployment"
git push origin main
```

### Step 2: Create Streamlit Cloud App
1. Visit https://share.streamlit.io
2. Click **"New app"** button
3. Sign in with GitHub (if not already)
4. Select your repository
5. Select the **main** branch
6. Set main file path to: `frontend/dashboard.py`
7. Click **"Deploy"**

The app will start deploying. This may take 1-2 minutes.

### Step 3: Add API Secrets (Critical!)
Once deployed, go to:
1. App hamburger menu (≡) → **"Settings"**
2. Click **"Secrets"** tab
3. Paste your secrets in TOML format:

```toml
GROQ_API_KEY = "gsk_xxxxxxxxxxxxx"
PINECONE_API_KEY = "xxxxxxxxxxxxx"
PINECONE_ENVIRONMENT = "gcp-starter"
```

4. Click **"Save"**

The app will automatically restart with the secrets.

### Step 4: Verify Deployment
1. Wait for the app to load
2. The dashboard should automatically run the scoring engine on first startup
3. You should see the compliance audit results display

---

## Git Preparation (Before Step 1)

Make sure these files are in your repository:

### Required in Repository:
- `requirements.txt` - Python dependencies
- `frontend/dashboard.py` - Main Streamlit app
- `backend/scoring_engine.py` - Scoring logic
- `backend/rag_compliance.py` - RAG system
- `data/3_labeled_dialogue.txt` - Sample data for analysis
- `data/policy.txt` - Compliance policies
- `.streamlit/config.toml` - Configuration file
- `.streamlit/secrets.toml.example` - Secrets template (for reference only)

### NOT in Repository (Ignored):
- `.streamlit/secrets.toml` - Your actual secrets (ignored by .gitignore)
- `.env` - Local environment variables
- `__pycache__/` - Python cache
- Virtual environment folders

---

## API Keys Required

Before deployment, obtain these API keys:

### 1. **Groq API Key**
- Visit: https://console.groq.com/keys
- Create/copy your API key
- Format: `gsk_xxxxxxxxxxxxx`

### 2. **Pinecone API Key** (If using Pinecone)
- Visit: https://app.pinecone.io/
- Create an index called `compliance-rules`
- Copy your API key
- Note your Pinecone environment (e.g., `gcp-starter`)

---

## Troubleshooting

### "audit_results.csv not found"
- The scoring engine should auto-run on first startup
- Check app logs in Streamlit Cloud dashboard for errors
- Ensure `data/3_labeled_dialogue.txt` exists in the repository

### API Key errors
- Verify secrets are added correctly in Settings → Secrets
- Check that key names match exactly: `GROQ_API_KEY`, `PINECONE_API_KEY`
- Restart the app after adding secrets

### Slow initial load
- First run processes all dialogue data (takes 1-2+ minutes depending on data size)
- This is normal. Subsequent loads will be faster due to caching.

### Module import errors
- Ensure all packages in `requirements.txt` are compatible with Python 3.8+
- Check the build logs in Streamlit Cloud for specific errors

---

## Post-Deployment

### Share Your App
After deployment, your app URL will be:
```
https://share.streamlit.io/[your-username]/[repo-name]/[branch]/frontend/dashboard.py
```

You can share this link with stakeholders. Anyone can access it without installing anything.

### Manage Your App
In Streamlit Cloud dashboard:
- View app logs
- Manage secrets
- Configure GitHub branch/directory
- Set rerun rate
- Archive/delete app

### Update Your App
Simply push changes to your GitHub repository - Streamlit Cloud will automatically redeploy!

```bash
# Make changes locally
git add .
git commit -m "Update dashboard features"
git push origin main
# App auto-redeploys within 1-2 minutes
```

---

## Security Notes

✅ **API Keys are secure:**
- Secrets stored in Streamlit Cloud's encrypted backend
- Never exposed in code or logs
- Never transmitted except to API services

✅ **Not committed to Git:**
- `.streamlit/secrets.toml` is in `.gitignore`
- Only the `.example` template is in git

✅ **Environment isolation:**
- Each deployment has its own secure environment
- No exposure to other users' apps

---

## Next Steps

1. Ensure all changes are committed to Git
2. Follow "Deployment Steps" above
3. Add your API secrets in Streamlit Cloud Settings
4. Share the app link with your team!

Good luck! 🚀
