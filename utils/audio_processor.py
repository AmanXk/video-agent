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