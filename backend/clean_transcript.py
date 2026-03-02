import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def label_speakers(transcript_text):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    prompt = f"""
    You are an expert at diarizing customer service transcripts. 
    Below is a raw transcript of a customer service call. 
    Separate it into a dialogue between an 'Agent' and a 'Customer'.
    
    Rules:
    1. Identify who is speaking based on the context:
       - Agent: Asks "How can I help?", provides solutions, uses professional language, identifies as company rep.
       - Customer: Explains issues, asks for help, provides personal/account details.
    2. Format EXACTLY as:
       Agent: [text]
       Customer: [text]
    3. CRITICAL: Each person's turn MUST be on a SINGLE LINE. Do not use newlines within a single speaker's turn.
    4. Do not add any preamble, commentary, or summary. Only the labeled dialogue.
    5. Maintain original wording as much as possible.
    
    Transcript:
    {transcript_text}
    """
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    with open("1_raw_transcript.txt", "r", encoding="utf-8") as f:
        content = f.read()
    labeled = label_speakers(content)
    with open("3_labeled_dialogue.txt", "w", encoding="utf-8") as f:
        f.write(labeled)
    print("Step 3 Complete: 3_labeled_dialogue.txt created.")
