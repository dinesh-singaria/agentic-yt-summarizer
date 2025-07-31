from transcriber import transcribe_audio

if __name__ == "__main__":
    transcript = transcribe_audio("downloads/AKJfakEsgy0.mp3")
    print("\n✅ Transcription Complete:\n")
    print(transcript)