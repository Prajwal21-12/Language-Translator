# Talkora — Professional Language Translator

A Streamlit-based multilingual translation web application.

## Features
- 14 language options
- Source and target language selection
- One-click language swapping
- Translation result display
- Recent translation history (up to 10 items per session)
- Input validation and error handling
- Responsive, styled interface

## Tech stack
Python, Streamlit, Requests, Google Translate web endpoint (unofficial), MyMemory API fallback.

## Run on Windows
```powershell
python -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```
Open the local URL printed in the terminal, usually http://localhost:8501.

## Important
The Google endpoint used here is unofficial and may change or be rate-limited. MyMemory is a fallback and is subject to provider limits. Translation quality can vary; verify important translations with a fluent speaker.

CodeAlpha Artificial Intelligence Internship — Task 1: Language Translation Tool.
