import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def transcribe_audio(audio_path, language=None):
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables.")
        
    client = Groq(api_key=api_key)
    
    try:
        print(f"Transcribing {audio_path} via Groq Cloud... (Language: {language if language else 'Auto-detect'})")
        with open(audio_path, "rb") as file:
            # Prepare transcription arguments
            transcription_args = {
                "file": (os.path.basename(audio_path), file.read()),
                "model": "whisper-large-v3",
                "response_format": "json"
            }
            if language and language.lower() != "auto-detect":
                transcription_args["language"] = language.lower()
                
            transcription = client.audio.transcriptions.create(**transcription_args)
        return transcription.text
    except Exception as e:
        print(f"Error during cloud transcription: {str(e)}")
        raise e

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python transcribe.py <path_to_audio>")
        sys.exit(1)
        
    audio_file = sys.argv[1]
    try:
        text = transcribe_audio(audio_file)
        # Use absolute path to ensure data is saved in the right place
        PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_path = os.path.join(PROJECT_ROOT, "data", "1_raw_transcript.txt")
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Step 1 Complete: {output_path} created.")
    except Exception as e:
        print(f"Transcription failed: {e}")
