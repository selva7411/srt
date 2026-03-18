import whisper
from deep_translator import GoogleTranslator
import sys
import os

# -------- SETTINGS --------
MODEL_SIZE = "base"   # change to "medium" or "large" for better accuracy
SOURCE_LANG = "ja"
TARGET_LANG = "en"

# -------- INPUT --------
if len(sys.argv) < 2:
    print("Usage: python generate_subtitles.py <video_file>")
    sys.exit(1)

video_file = sys.argv[1]
output_srt = os.path.splitext(video_file)[0] + "_en.srt"

# -------- LOAD MODEL --------
print("🔄 Loading Whisper model...")
model = whisper.load_model(MODEL_SIZE)

# -------- TRANSCRIBE --------
print("🎧 Transcribing Japanese audio...")
result = model.transcribe(video_file, language=SOURCE_LANG)

segments = result["segments"]

# -------- FORMAT TIME --------
def format_time(seconds):
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hrs:02}:{mins:02}:{secs:02},{millis:03}"

# -------- TRANSLATE + WRITE SRT --------
print("🌐 Translating and creating SRT...")

with open(output_srt, "w", encoding="utf-8") as f:
    for i, seg in enumerate(segments, start=1):
        start = format_time(seg["start"])
        end = format_time(seg["end"])
        jp_text = seg["text"].strip()

        try:
            en_text = GoogleTranslator(source=SOURCE_LANG, target=TARGET_LANG).translate(jp_text)
        except:
            en_text = jp_text  # fallback

        f.write(f"{i}\n")
        f.write(f"{start} --> {end}\n")
        f.write(en_text + "\n\n")

print(f"\n✅ Done! Subtitle saved as: {output_srt}")