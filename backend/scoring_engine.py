import os
import sys
import pandas as pd
import json
from groq import Groq
from rag_compliance import ComplianceRAG

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
rag_system = ComplianceRAG()

def score_chunk(chunk_text):
    # Retrieve specific rules for this part of the talk
    relevant_rules = rag_system.get_rules_for_context(chunk_text)
    
    prompt = f"""
    Evaluate this chunk based on these specific rules:
    {relevant_rules}

    Conversation:
    {chunk_text}

    Return JSON ONLY:
    {{
      "empathy": 1-100,
      "professionalism": 1-100,
      "compliance": "Pass/Fail/Warn",
      "reason": "Explain violation if any",
      "violations": ["List specific policy violations"],
      "suggestions": ["List specific improvement suggestions"]
    }}
    """
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        response_format={ "type": "json_object" }
    )
    return json.loads(response.choices[0].message.content)

def run_average_audit(file_path):
    with open(file_path, "r") as f:
        lines = f.readlines()

    # Process in chunks of 5 turns
    chunk_results = []
    for i in range(0, len(lines), 5):
        chunk = "".join(lines[i:i+5])
        chunk_results.append(score_chunk(chunk))

    # Create DataFrame with chunk results
    df = pd.DataFrame(chunk_results)
    
    # Add chunk numbers for clarity
    df.insert(0, 'Chunk', range(1, len(df) + 1))
    
    # Convert violations and suggestions lists to strings for CSV
    if 'violations' in df.columns:
        df['violations'] = df['violations'].apply(lambda x: ' | '.join(x) if isinstance(x, list) else str(x))
    if 'suggestions' in df.columns:
        df['suggestions'] = df['suggestions'].apply(lambda x: ' | '.join(x) if isinstance(x, list) else str(x))
    
    # Calculate averages
    final_empathy = df['empathy'].mean()
    final_professionalism = df['professionalism'].mean()
    
    # Determine overall compliance
    if "Fail" in df['compliance'].values:
        overall_compliance = "FAIL"
    elif "Warn" in df['compliance'].values:
        overall_compliance = "WARN"
    else:
        overall_compliance = "PASS"
    
    # Aggregate violations and suggestions
    all_violations = []
    all_suggestions = []
    
    if 'violations' in df.columns:
        for vuln_str in df['violations']:
            if pd.notna(vuln_str):
                all_violations.extend([v.strip() for v in str(vuln_str).split('|')])
    
    if 'suggestions' in df.columns:
        for sugg_str in df['suggestions']:
            if pd.notna(sugg_str):
                all_suggestions.extend([s.strip() for s in str(sugg_str).split('|')])
    
    # Remove duplicates
    all_violations = list(set([v for v in all_violations if v]))
    all_suggestions = list(set([s for s in all_suggestions if s]))
    
    # Create final results row
    final_row = pd.DataFrame([{
        'Chunk': 'FINAL',
        'empathy': final_empathy,
        'professionalism': final_professionalism,
        'compliance': overall_compliance,
        'reason': 'Final average scores',
        'violations': ' | '.join(all_violations) if all_violations else 'None',
        'suggestions': ' | '.join(all_suggestions) if all_suggestions else 'None'
    }])
    
    # Append final row to dataframe
    df = pd.concat([df, final_row], ignore_index=True)
    
    # Save to CSV
    csv_filename = "../data/audit_results.csv"
    df.to_csv(csv_filename, index=False)
    print(f"\nCSV file saved: {csv_filename}")
    
    # Print results
    print("\n--- FINAL AUDIT RESULTS ---")
    print(f"Final Empathy Score: {final_empathy}")
    print(f"Final Professionalism Score: {final_professionalism}")
    print(f"Overall Compliance: {overall_compliance}")
    
    return df

run_average_audit("../data/3_labeled_dialogue.txt")
