import yt_dlp
from pydub import AudioSegment
import os

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
def download_audio(url: str) -> str:
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(DOWNLOAD_DIR, '%(id)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        audio_file = ydl.prepare_filename(info_dict).replace('.webm', '.wav').replace('.m4a', '.wav')
        return audio_file
    

def convert_to_wav(input_path: str) -> str:
    """
    Convert an audio file to WAV format using pydub.
    """
    output_path = os.path.splitext(input_path)[0] + '_converted.wav'
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_frame_rate(16000).set_channels(1)
    audio.export(output_path, format='wav')
    return output_path


def chunk_audio(input_path: str, chunk_minutes: int = 10) -> list:
    """
    Chunk an audio file into smaller segments.
    """
    chunk_length_ms = chunk_minutes * 60 * 1000
    audio = AudioSegment.from_file(input_path)
    chunks = []
    for i in range(0, len(audio), chunk_length_ms):
        chunk = audio[i:i + chunk_length_ms]
        chunk_path = f"{os.path.splitext(input_path)[0]}_chunk_{i//chunk_length_ms}.wav"
        chunk.export(chunk_path, format='wav')
        chunks.append(chunk_path)
    return chunks

def process_input(source: str) -> list:
    """
    Process the input source, which can be a URL or a local file path.
    """
    if source.startswith("http://") or source.startswith("https://"):
        print('detected url, downloading audio...')
        audio_path = download_audio(source)
    else:
        print('detected local file, processing audio...')
        audio_path = convert_to_wav(source)
    print('chunking audio...')
    chunks = chunk_audio(audio_path)
    print(f'audio raedy - {len(chunks)} chunks created')
    return chunks