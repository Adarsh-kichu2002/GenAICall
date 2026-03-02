import os
import sys
import logging
from transcribe import transcribe_audio
from clean_transcript import label_speakers
from scoring_engine import run_average_audit
from dotenv import load_dotenv

load_dotenv()

# Get the project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_pipeline(audio_path, agent_name="Unknown Agent"):
    # Ensure data directory exists
    data_dir = os.path.join(PROJECT_ROOT, "data")
    os.makedirs(data_dir, exist_ok=True)
    
    try:
        # 1. Transcribe
        logger.info(f"Starting transcription for {audio_path}")
        raw_text = transcribe_audio(audio_path)
        
        raw_transcript_path = os.path.join(data_dir, "1_raw_transcript.txt")
        with open(raw_transcript_path, "w", encoding="utf-8") as f:
            f.write(raw_text)
        logger.info(f"Transcription complete. Saved to {raw_transcript_path}")

        # 2. Label Speakers (Diarization)
        logger.info("Starting speaker labeling...")
        labeled_text = label_speakers(raw_text)
        
        labeled_transcript_path = os.path.join(data_dir, "3_labeled_dialogue.txt")
        with open(labeled_transcript_path, "w", encoding="utf-8") as f:
            f.write(labeled_text)
        logger.info(f"Speaker labeling complete. Saved to {labeled_transcript_path}")

        # 3. Score
        logger.info("Starting compliance scoring...")
        run_average_audit(labeled_transcript_path, agent_name=agent_name)
        logger.info(f"Scoring complete for {agent_name}. audit_results.csv updated.")
        
        return True
    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pipeline.py <path_to_audio> [agent_name]")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    agent_name = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(os.path.basename(audio_file))[0]
    
    success = run_pipeline(audio_file, agent_name)
    if success:
        print("Pipeline finished successfully!")
    else:
        print("Pipeline failed.")
