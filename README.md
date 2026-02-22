# Compliance Audit System

A comprehensive compliance audit dashboard for analyzing agent performance against policy violations.

## Project Structure

```
d:\customer\
├── frontend/                    # Streamlit Dashboard Application
│   ├── dashboard.py            # Main dashboard application (loads from ../data/audit_results.csv)
│   └── .streamlit/
│       └── config.toml         # Streamlit dark mode configuration
│
├── backend/                     # Backend Processing Scripts
│   ├── rag_compliance.py       # Compliance RAG system with mock embeddings
│   ├── scoring_engine.py       # Score chunks against policies (reads from ../data/3_labeled_dialogue.txt)
│   ├── upload_policies.py      # Upload policies to Pinecone (reads from ../data/policy.txt)
│   ├── clean_transcript.py     # Transcript cleaning utility
│   ├── transcribe.py           # Transcription utility
│   └── Transcript_Preprocessing.ipynb  # Jupyter notebook for preprocessing
│
├── data/                        # Input Data and Output Files
│   ├── 1_raw_transcript.txt    # Original transcript
│   ├── 2_cleaned_transcript.txt # Cleaned transcript
│   ├── 3_labeled_dialogue.txt  # Labeled dialogue for scoring
│   ├── policy.txt              # Compliance policies
│   └── audit_results.csv       # Generated audit scores (output)
│
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables (API keys)
└── README.md                    # This file
```

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables in `.env`:
```
GROQ_API_KEY=your_groq_api_key
PINECONE_API_KEY=your_pinecone_api_key
```

## Usage

### 1. Upload Policies 
```bash
python backend/upload_policies.py
```
This uploads compliance policies from `data/policy.txt` to Pinecone for RAG retrieval.

### 2. Score Chunks
```bash
python backend/scoring_engine.py
```
This processes `data/3_labeled_dialogue.txt`, scores each chunk against policies, and generates `data/audit_results.csv`.

### 3. Run Dashboard
```bash
cd frontend
streamlit run dashboard.py
```
This starts the interactive compliance audit dashboard at http://localhost:8501

## Dashboard Features

- **Home Page**: Overall compliance scores, top violations, and improvement suggestions
- **Reports Page**: Trend analysis, compliance distribution pie chart, and detailed results table
- **Chunk-wise Analysis**: Per-chunk scores with specific violations and suggestions

## API Keys Required

- **Groq API**: For LLM-based compliance scoring
- **Pinecone API**: For vector database 
## Notes

- The system uses mock embeddings by default to avoid external model download issues
- All file paths are relative and should work when running scripts from the appropriate directories
- The dashboard auto-generates charts and exports CSV results for further analysis
