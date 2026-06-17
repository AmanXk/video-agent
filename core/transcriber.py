import whisper
import os
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "small")

_model = None

def load_model():
    global _model
    if _model is None:
        print(f'loading whisper model: {_model}...')
        _model = whisper.load_model(WHISPER_MODEL)
    return _model

def transcribe_chunk(chunk_path: str, translate: bool = False) -> str:
    model = load_model()
    task = "translate" if translate else "transcribe"
    result = model.transcribe(chunk_path,task=task)
    return result['text']

def transcribe_all(chunks: list, translate: bool = False) -> str:
    full_transcription = ""
    for chunk in chunks:
        print(f'transcribing chunk: {chunk}...')
        text = transcribe_chunk(chunk, translate)
        full_transcription += text+" "
    print("transcription complete.")
    return full_transcription.strip()