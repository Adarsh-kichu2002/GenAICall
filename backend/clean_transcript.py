import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# 1. LOAD: Read the cleaned text from the Notebook
with open("2_cleaned_transcript.txt", "r") as f:
    content = f.read()

# 2. PROCESS: Ask Groq to label speakers
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": f"Format this into a dialogue with 'Agent:' and 'Customer:':\n\n{content}"}]
)

# 3. SAVE: The final labeled dialogue
with open("3_labeled_dialogue.txt", "w") as f:
    f.write(response.choices[0].message.content)

print("Step 3 Complete: 3_labeled_dialogue.txt created.")
