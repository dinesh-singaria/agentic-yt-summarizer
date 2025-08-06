from keyframe_extractor import extract_keyframes_from_video_url

video_url = "https://www.youtube.com/watch?v=Ih1LDnPijFU&t=64s"  # Replace with a real video

frames = extract_keyframes_from_video_url(video_url)

print("✅ Extracted Keyframes:")
for path in frames:
    print(path)