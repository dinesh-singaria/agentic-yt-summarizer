import os
import uuid
import cv2
from scenedetect import VideoManager, SceneManager
from scenedetect.detectors import ContentDetector
import yt_dlp

def download_video(video_url: str, downloads_dir: str = "downloads") -> str:
    os.makedirs(downloads_dir, exist_ok=True)
    base_filename = str(uuid.uuid4())
    output_template = os.path.join(downloads_dir, base_filename + ".%(ext)s")
    video_path = os.path.join(downloads_dir, base_filename + ".mp4")

    ydl_opts = {
        'format': 'best[height<=480]+bestaudio/best',
        'outtmpl': output_template,
        'merge_output_format': 'mp4',
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    if not os.path.exists(video_path):
        raise RuntimeError("❌ Video file missing after download")

    return video_path


def extract_keyframes(video_path: str, output_dir: str = "keyframes", threshold: float = 90.0) -> list:
    os.makedirs(output_dir, exist_ok=True)

    video_manager = VideoManager([video_path])
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector(threshold=threshold))
    base_timecode = video_manager.get_base_timecode()

    video_manager.set_downscale_factor()
    video_manager.start()
    scene_manager.detect_scenes(frame_source=video_manager)

    scene_list = scene_manager.get_scene_list(base_timecode)
    cap = cv2.VideoCapture(video_path)
    keyframe_paths = []

    for idx, (start, end) in enumerate(scene_list):
        mid_time = (start.get_seconds() + end.get_seconds()) / 2
        cap.set(cv2.CAP_PROP_POS_MSEC, mid_time * 1000)
        success, frame = cap.read()
        if success:
            frame_path = os.path.join(output_dir, f"scene_{idx+1}.jpg")
            cv2.imwrite(frame_path, frame)
            keyframe_paths.append(frame_path)

    cap.release()
    video_manager.release()
    return keyframe_paths


def extract_keyframes_from_video_url(video_url: str) -> list:
    print("🎞️ Downloading video...")
    video_path = download_video(video_url)

    print("🔍 Extracting keyframes...")
    keyframes = extract_keyframes(video_path)

    print("🧹 Cleaning up video file...")
    os.remove(video_path)

    # Convert local paths to web-accessible URLs
    base_url = "http://localhost:5050"  # Replace with your actual frontend base if different
    keyframe_urls = [f"{base_url}/keyframes/{os.path.basename(path)}" for path in keyframes]

    return keyframe_urls