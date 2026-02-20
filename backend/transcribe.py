import whisper

model = whisper.load_model("base")
print("Transcribing... please wait.")
result = model.transcribe("sample.mp3", fp16=False) 

# SAVE THE BATON: Write to a file so the Notebook can find it
with open("1_raw_transcript.txt", "w", encoding="utf-8") as f:
    f.write(result["text"])

print("Step 1 Complete: 1_raw_transcript.txt created.")
