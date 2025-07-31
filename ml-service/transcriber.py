import whisper

# Load the tiny model (first time will download to ~/.cache/whisper)
model = whisper.load_model("tiny")

def transcribe_audio(audio_path: str) -> str:
    """
    Transcribes an audio file using OpenAI's Whisper tiny model.
    
    Parameters:
        audio_path (str): Path to the audio file (.mp3, .wav, .m4a, etc.)

    Returns:
        str: Full transcript text
    """
    result = model.transcribe(audio_path)
    return result['text']