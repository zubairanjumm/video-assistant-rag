import yt_dlp
from pydub import AudioSegment
import os
import glob
import time

DOWNLOAD_DIR = 'downloads'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def download_youtube_audio(url: str) -> str:
    output_path = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
        "quiet": True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
    except Exception as e:
        raise RuntimeError(f"Failed to download YouTube audio: {e}") from e

    title = info.get("title", "audio")
    safe_title = "".join(c if c.isalnum() or c in " -_" else "_" for c in title).strip()
    expected = os.path.join(DOWNLOAD_DIR, f"{safe_title}.wav")

    if os.path.exists(expected):
        return expected

    matches = glob.glob(os.path.join(DOWNLOAD_DIR, "*.wav"))
    if matches:
        return max(matches, key=os.path.getmtime)

    raise FileNotFoundError(
        f"Download completed but no .wav file found in '{DOWNLOAD_DIR}'."
    )


def convert_to_wav(input_path: str) -> str:
    try:
        audio = AudioSegment.from_file(input_path)
    except Exception as e:
        raise RuntimeError(f"Failed to load audio from '{input_path}': {e}") from e

    if len(audio) == 0:
        raise ValueError(f"Audio file '{input_path}' is empty or corrupt.")

    base, _ = os.path.splitext(input_path)
    output_path = f"{base}_converted_{int(time.time())}.wav"
    audio = audio.set_channels(1).set_frame_rate(16000)
    try:
        audio.export(output_path, format="wav")
    except Exception as e:
        raise RuntimeError(f"Failed to export WAV to '{output_path}': {e}") from e

    return output_path


def chunk_audio(wav_path: str, chunk_minutes: int = 10) -> list:
    try:
        audio = AudioSegment.from_wav(wav_path)
    except Exception as e:
        raise RuntimeError(f"Failed to load WAV '{wav_path}': {e}") from e

    if len(audio) == 0:
        raise ValueError(f"WAV file '{wav_path}' is empty.")

    chunk_ms = chunk_minutes * 60 * 1000
    chunks = []

    for i, start in enumerate(range(0, len(audio), chunk_ms)):
        chunk = audio[start: start + chunk_ms]
        chunk_path = f"{wav_path}_chunk_{i}_{int(time.time())}.wav"
        try:
            chunk.export(chunk_path, format="wav")
        except Exception as e:
            raise RuntimeError(f"Failed to export chunk '{chunk_path}': {e}") from e

        chunks.append(chunk_path)

    return chunks


def process_input(source: str) -> list:
    if source.startswith("http://") or source.startswith("https://"):
        print("Detected YouTube URL. Downloading audio...")
        wav_path = download_youtube_audio(source)
    else:
        print("Detected local file. Converting to WAV...")
        wav_path = convert_to_wav(source)

    print("Chunking audio...")
    chunks = chunk_audio(wav_path)
    print(f"Audio ready — {len(chunks)} chunk(s) created.")
    return chunks
