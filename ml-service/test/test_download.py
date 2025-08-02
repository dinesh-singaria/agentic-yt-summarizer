from audio_downloader import download_audio

if __name__ == '__main__':
    url = "https://www.youtube.com/watch?v=AKJfakEsgy0"  # Replace with any short video
    path = download_audio(url)
    print(f"✅ Audio saved at: {path}")