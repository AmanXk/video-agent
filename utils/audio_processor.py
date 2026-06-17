import yt_dlp
from pydub import AudioSegment
import os
import logging
logging.basicConfig(
    level = logging.INFO,
    format = '%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def download_audio(url: str) -> str:
    logger.info(f'Downloading audio from URL: {url}')
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        audio_file = ydl.prepare_filename(info_dict).replace('.webm', '.wav').replace('.m4a', '.wav')
        logger.info(f'Audio downloaded and converted to WAV: {audio_file}')
        return audio_file

def convert_to_wav(input_path: str) -> str:
    
    logger.info(f'Converting audio to WAV format:')
    output_path = os.path.splitext(input_path)[0] + '_converted.wav'
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_frame_rate(16000).set_channels(1)
    audio.export(output_path, format='wav')
    logger.info(f'Audio converted to WAV: {output_path}')
    return output_path

def chunk_audio(input_path: str, chunk_minutes: int = 10) -> list:
    logger.info(f'Chunking audio into {chunk_minutes}-minute segments...')
    chunk_length_ms = chunk_minutes * 60 * 1000
    audio = AudioSegment.from_file(input_path)
    chunks = []
    for i in range(0, len(audio), chunk_length_ms):
        chunk = audio[i:i + chunk_length_ms]
        chunk_path = f"{os.path.splitext(input_path)[0]}_chunk_{i//chunk_length_ms}.wav"
        chunk.export(chunk_path, format='wav')
        chunks.append(chunk_path)
    logger.info(f'Audio chunked into {len(chunks)} segments.')
    return chunks

def process_input(source: str) -> list:
    """
    Process the input source, which can be a URL or a local file path.
    """
    if source.startswith("http://") or source.startswith("https://"):
        logger.info('detected url, downloading audio...')
        audio_path = download_audio(source)
    else:
        logger.info('detected local file, processing audio...')
        audio_path = convert_to_wav(source)
    logger.info('chunking audio...')
    chunks = chunk_audio(audio_path)
    logger.info(f'audio ready - {len(chunks)} chunks created')
    return chunks
