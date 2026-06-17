from utils.audio_processor import process_input
from core.transcriber import transcribe_all

source = "https://www.youtube.com/watch?v=Lg-meK5IU8Q"  # Example URL

chunks = process_input(source)
print(f'Chunks created: {chunks}')
transcription = transcribe_all(chunks, translate=False) 
print(f'Transcription: {transcription}')