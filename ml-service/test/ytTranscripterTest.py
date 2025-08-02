from youtube_transcript_api import YouTubeTranscriptApi

def get_yt_transcript(video_id: str) -> str:
    fetched = YouTubeTranscriptApi().fetch(video_id)

    transcript = " ".join([snippet.text for snippet in fetched.snippets])
   
    return transcript

text = get_yt_transcript("kCc8FmEb1nY")
print(text[:500])  # Print first 500 characters


# from youtube_transcript_api import YouTubeTranscriptApi

# ytt_api = YouTubeTranscriptApi.fetch('kCc8FmEb1nY')


# transcript = ""
# for i in ytt_api:
#     transcript += "" + i["text"]

# print(transcript)
