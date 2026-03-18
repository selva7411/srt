import tkinter as tk
from tkinter import filedialog, messagebox
import whisper
from deep_translator import GoogleTranslator
import os

# Load model once
model = whisper.load_model("base")

def format_time(seconds):
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hrs:02}:{mins:02}:{secs:02},{millis:03}"

def generate_subtitles(file_path):
    try:
        status_label.config(text="🎧 Transcribing...")
        root.update()

        result = model.transcribe(file_path, language="ja")
        segments = result["segments"]

        output_srt = os.path.splitext(file_path)[0] + "_en.srt"

        status_label.config(text="🌐 Translating...")
        root.update()

        with open(output_srt, "w", encoding="utf-8") as f:
            for i, seg in enumerate(segments, start=1):
                start = format_time(seg["start"])
                end = format_time(seg["end"])
                jp_text = seg["text"].strip()

                try:
                    en_text = GoogleTranslator(source='ja', target='en').translate(jp_text)
                except:
                    en_text = jp_text

                f.write(f"{i}\n")
                f.write(f"{start} --> {end}\n")
                f.write(en_text + "\n\n")

        status_label.config(text="✅ Done!")
        messagebox.showinfo("Success", f"Subtitle created:\n{output_srt}")

    except Exception as e:
        messagebox.showerror("Error", str(e))
        status_label.config(text="❌ Error")

def browse_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("Video Files", "*.mp4 *.ts *.mkv")]
    )
    if file_path:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)

def start_process():
    file_path = file_entry.get()
    if not file_path:
        messagebox.showwarning("Warning", "Please select a file")
        return
    generate_subtitles(file_path)

# UI
root = tk.Tk()
root.title("Subtitle Generator")
root.geometry("500x200")

tk.Label(root, text="Select Video File").pack(pady=5)

file_entry = tk.Entry(root, width=50)
file_entry.pack(pady=5)

tk.Button(root, text="Browse", command=browse_file).pack(pady=5)
tk.Button(root, text="Generate Subtitles", command=start_process).pack(pady=10)

status_label = tk.Label(root, text="Idle")
status_label.pack(pady=10)

root.mainloop()