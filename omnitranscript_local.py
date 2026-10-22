"""
LocalPulse AI / OmniTranscript Local
-------------------------------------
100% Offline Speech-to-Text & Local Knowledge Mining Pipeline.
Uses OpenAI Whisper for local transcription and Ollama (Llama 3/Mistral)
for executive summarization and action item extraction.

License: MIT
"""

import os
import sys
import json
import argparse
import urllib.request
import whisper

# Configurare implicită Ollama Local API
OLLAMA_API_URL = "http://localhost:11434/api/generate"
DEFAULT_OLLAMA_MODEL = "llama3"

SYSTEM_PROMPT = """
You are an expert AI executive assistant. Analyze the provided transcript of a meeting, 
interview, or lecture and produce a structured summary in Markdown format.

Structure your response as follows:
1. ## Executive Summary
   - A concise 2-3 sentence overview of the discussion.
2. ## Key Topics & Discussion Points
   - Bullet points of the main ideas discussed.
3. ## Action Items & Responsibilities
   - List tasks assigned, next steps, and responsible parties (if mentioned).
4. ## Questions & Unresolved Issues
   - Any open questions or pending decisions.

Transcript:
"""

def check_ollama_status() -> bool:
    """Verifică dacă serviciul local Ollama rulează."""
    try:
        req = urllib.request.Request("http://localhost:11434/api/tags")
        with urllib.request.urlopen(req, timeout=3) as response:
            return response.status == 200
    except Exception:
        return False

def transcribe_audio(file_path: str, model_size: str = "base") -> str:
    """
    Transcrie fișierul audio/video utilizând modelul Whisper local.
    Model sizes: 'tiny', 'base', 'small', 'medium', 'large'
    """
    print(f"[1/3] Loading local Whisper model ('{model_size}')...")
    model = whisper.load_model(model_size)
    
    print(f"[2/3] Transcribing audio file: {file_path} ...")
    result = model.transcribe(file_path, verbose=False)
    
    transcript_text = result.get("text", "").strip()
    print(f"[SUCCESS] Transcription complete ({len(transcript_text)} characters).")
    return transcript_text

def summarize_with_ollama(transcript: str, model_name: str = DEFAULT_OLLAMA_MODEL) -> str:
    """
    Trimite transcrierea către Ollama local pentru rezumat și extagerea de task-uri.
    """
    print(f"[3/3] Generating summary & action items using local Ollama model ('{model_name}')...")
    
    payload = {
        "model": model_name,
        "prompt": f"{SYSTEM_PROMPT}\n{transcript}",
        "stream": False
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_API_URL, 
        data=data, 
        headers={"Content-Type": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            return res_data.get("response", "No response generated.")
    except Exception as e:
        print(f"[WARNING] Could not connect to Ollama ({e}). Returning raw transcript only.")
        return "*(Ollama local summarization unavailable. Ensure Ollama is running on port 11434)*"

def save_markdown_report(audio_path: str, transcript: str, summary: str):
    """Salvează rezultatul final într-un fișier Markdown."""
    base_name = os.path.splitext(os.path.basename(audio_path))[0]
    output_filename = f"{base_name}_LocalPulse_Report.md"
    
    content = f"""# LocalPulse AI - Audio Analysis Report
**Source File:** `{os.path.basename(audio_path)}`  
**Privacy Status:** 100% Offline / Local Processing  

---

{summary}

---

## Full Audio Transcript
```text
{transcript}
