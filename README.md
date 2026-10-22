# LocalPulse-AI-sau-OmniTranscript-Local-Un-Hub-Local-Privat-de-Transcriere-Rezumare-i-Minare-
Într-o eră în care toată lumea folosește instrumente cloud pentru transcrieri (care costă bani și pun probleme de confidențialitate), tot mai mulți dezvoltatori și utilizatori își doresc alternative local-first, care rulează direct pe hardware-ul propriu (GPU/CPU), protejând datele personale sau de business (ședințe, interviuri, cursuri


Acest script este conceput modular și 100% offline:

Prelucrează fișiere audio/video (MP3, WAV, MP4).

Transcrie audio-ul local folosind Whisper.

Trimite textul către Ollama (care rulează un model local precum llama3 sau mistral) pentru a genera rezumatul executiv și lista de task-uri (Action Items).

Salvează totul automat într-un fișier curat în format Markdown.


"""
with open(output_filename, "w", encoding="utf-8") as f:
f.write(content)

print(f"\n[DONE] Full report successfully saved to: {output_filename}")
def main():
parser = argparse.ArgumentParser(description="LocalPulse AI - Offline Audio Transcription & Knowledge Mining")
parser.add_argument("file", help="Path to audio/video file (MP3, WAV, MP4, MKV)")
parser.add_argument("--whisper-model", default="base", choices=["tiny", "base", "small", "medium", "large"], help="Whisper model size")
parser.add_argument("--ollama-model", default="llama3", help="Local Ollama model name (e.g., llama3, mistral, gemma)")

args = parser.parse_args()

if not os.path.exists(args.file):
    print(f"[ERROR] File not found: {args.file}")
    sys.exit(1)
    
print("=" * 60)
print("      LOCALPULSE AI / OMNITRANSCRIPT LOCAL (OFFLINE)")
print("=" * 60)

# Check Ollama
if check_ollama_status():
    print("[STATUS] Local Ollama service detected and active.")
else:
    print("[STATUS] Local Ollama service not detected. Will process transcript without LLM summary.")
    
# Process
transcript = transcribe_audio(args.file, model_size=args.whisper-model)
summary = summarize_with_ollama(transcript, model_name=args.ollama-model)

# Save Report
save_markdown_report(args.file, transcript, summary)
if name == "main":
main()


---

### Cum se rulează (Cerințe & Comenzi)

1. **Instalare dependențe Python:**
   ```bash
   pip install openai-whisper
Rularea aplicației:

Bash
python omnitranscript_local.py sedinta_echipa.mp3 --whisper-model base --ollama-model llama3
Scriptul generează automat un fișier Markdown (ex. sedinta_echipa_LocalPulse_Report.md) complet structurat, funcționând integral pe calculatoare fără conexiune la internet.
