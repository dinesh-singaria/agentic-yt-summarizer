# import whisper

# # Load the tiny model (first time will download to ~/.cache/whisper)
# model = whisper.load_model("tiny")

# def transcribe_audio(audio_path: str) -> str:
#     """
#     Transcribes an audio file using OpenAI's Whisper tiny model.
    
#     Parameters:
#         audio_path (str): Path to the audio file (.mp3, .wav, .m4a, etc.)

#     Returns:
#         str: Full transcript text
#     """
#     result = model.transcribe(audio_path)
#     return result['text']


import os
import uuid
import re
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
import whisper

# Load Whisper model once
whisper_model = whisper.load_model("tiny")

def get_youtube_transcript(video_url: str) -> str:
    match = re.search(r"(?:v=|youtu\.be/)([^&]+)", video_url)
    if not match:
        raise ValueError("❌ Invalid YouTube URL")

    video_id = match.group(1)
    fetched = YouTubeTranscriptApi().fetch(video_id)
    transcript = " ".join([snippet.text for snippet in fetched.snippets])
   
    return transcript


def download_audio(video_url: str, downloads_dir: str) -> str:
    os.makedirs(downloads_dir, exist_ok=True)
    base_filename = str(uuid.uuid4())
    output_template = os.path.join(downloads_dir, base_filename + ".%(ext)s")
    audio_path = os.path.join(downloads_dir, base_filename + ".mp3")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_template,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    if not os.path.exists(audio_path):
        raise RuntimeError("❌ Audio file missing after download")

    return audio_path


def get_whisper_transcript(video_url: str) -> str:
    downloads_dir = "downloads"
    audio_path = download_audio(video_url, downloads_dir)

    result = whisper_model.transcribe(audio_path)
    os.remove(audio_path)
    return result["text"]


def get_transcript(video_url: str) -> str:
    try:
        print("⚡ Trying YouTube Transcript API...")
        return get_youtube_transcript(video_url)
    except Exception as e1:
        print("⚠️ Failed to get YouTube transcript:", e1)
        print("🧠 Falling back to Whisper...")
        try:
            return get_whisper_transcript(video_url)
        except Exception as e2:
            print("❌ Whisper transcription also failed:", e2)
            raise RuntimeError("Failed to fetch transcript from both sources.")