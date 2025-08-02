from transcriber import get_transcript

# 🔗 Replace with any YouTube video link you want to test
test_url = "https://www.youtube.com/watch?v=kCc8FmEb1nY"

try:
    print("🎬 Getting transcript for:", test_url)
    transcript = get_transcript(test_url)
    print("\n📜 Transcript (first 500 characters):\n")
    print(transcript[:500])
except Exception as e:
    print("❌ Error during transcription test:", e)


# from youtube_transcript_api import YouTubeTranscriptApi

# ytt_api = YouTubeTranscriptApi()
# fetched_transcript = ytt_api.fetch('kCc8FmEb1nY')

# for snippet in fetched_transcript:
#     print(snippet.text)
