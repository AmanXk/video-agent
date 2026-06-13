# Audio Processing Utilities

This module provides utility functions for downloading audio from YouTube, converting audio files to a standardized WAV format, and splitting long audio recordings into smaller chunks. It is intended to be used as a preprocessing component in audio analysis, speech recognition, and transcription workflows.

## Features

* Download audio from YouTube videos using `yt-dlp`
* Extract audio in WAV format using FFmpeg
* Convert audio files to a standard format (16 kHz, mono)
* Split large audio files into smaller chunks
* Automatic management of the download directory

## Dependencies

Install the required packages:

```bash
pip install yt-dlp pydub
```

FFmpeg must be installed and accessible from the system PATH.

Verify the installation:

```bash
ffmpeg -version
```

## Functions

### `download_audio(url: str) -> str`

Downloads the best available audio stream from a YouTube video and converts it to WAV format.

**Parameters**

| Parameter | Type | Description       |
| --------- | ---- | ----------------- |
| url       | str  | YouTube video URL |

**Returns**

* Path to the downloaded WAV file.

**Example**

```python
audio_path = download_audio(
    "https://www.youtube.com/watch?v=VIDEO_ID"
)
```

---

### `convert_to_wav(input_path: str) -> str`

Converts an audio file to WAV format and standardizes it for downstream processing.

The output audio is configured with:

* Sample Rate: 16000 Hz
* Channels: Mono

**Parameters**

| Parameter  | Type |
| ---------- | ---- |
| input_path | str  |

**Returns**

* Path to the converted WAV file.

**Example**

```python
wav_path = convert_to_wav("meeting.mp3")
```

---

### `chunk_audio(input_path: str, chunk_minutes: int = 10) -> list`

Splits an audio file into smaller WAV segments of a specified duration.

**Parameters**

| Parameter     | Type | Description                       |
| ------------- | ---- | --------------------------------- |
| input_path    | str  | Path to the audio file            |
| chunk_minutes | int  | Duration of each chunk in minutes |

**Returns**

* List containing paths to the generated chunk files.

**Example**

```python
chunks = chunk_audio(
    "meeting.wav",
    chunk_minutes=5
)
```

## Example Usage

```python
url = "https://www.youtube.com/watch?v=VIDEO_ID"

audio_file = download_audio(url)

wav_file = convert_to_wav(audio_file)

chunks = chunk_audio(
    wav_file,
    chunk_minutes=10
)

print(chunks)
```

## Project Structure

```text
.
├── downloads/
├── audio_utils.py
└── README.md
```

## Output Example

```text
downloads/
├── abc123.wav
├── abc123_converted.wav
├── abc123_converted_chunk_0.wav
├── abc123_converted_chunk_1.wav
└── abc123_converted_chunk_2.wav
```

## Technologies

* Python
* yt-dlp
* FFmpeg
* pydub

## License

This project is licensed under the MIT License.
