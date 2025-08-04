from flask_cors import CORS
from flask import Flask, request, jsonify
from summarizer import summarize
from transcriber import get_transcript
from chapter_segmenter import segment_into_chapters, parse_chapters 


app = Flask(__name__)
CORS(app)

@app.route('/summarize', methods=['POST'])
def summarize_route():
    data = request.get_json()
    video_url = data.get('videoUrl')
    prompt = data.get('prompt') or "Summarize this video"

    print("✅ Received request with URL:", video_url)
    print("📝 Prompt:", prompt)

    # Step 1: Transcript
    print("🎬 Step 1: Getting transcript (YT API or Whisper fallback)...")
    try:
        transcript = get_transcript(video_url)
        print("✅ Transcript (first 150 chars):", transcript[:150], "...")
    except Exception as e:
        print("❌ Transcript failed:", str(e))
        return jsonify({"error": f"Transcript failed: {str(e)}"}), 500
    
    # Step 2: Summarize
    print("🧠 Step 2: Generating summary...")
    try:
        summary = summarize(transcript, prompt)
        print("✅ Summary:", summary)
    except Exception as e:
        print("❌ Summarization failed:", str(e))
        return jsonify({"error": f"Summarization failed: {str(e)}"}), 500


    # Step 3: Chapter Segmentation
    print("📚 Step 3: Segmenting into chapters...")
    try:
        raw_chapter_text = segment_into_chapters(transcript)
        chapters = parse_chapters(raw_chapter_text)
        print("✅ Chapters segmented successfully.")
        print("📖 First Chapter:", chapters[0] if chapters else "No chapters found", "\n")
    except Exception as e:
        print("❌ Chapter segmentation error:", str(e))
        return jsonify({"error": f"Chapter segmentation failed: {str(e)}"}), 500
    print("🚀 Done! Returning response.")

    return jsonify({
        "summary": summary,
        "chapters": chapters,
        "keyframes": [],
        "audio": []
    })

if __name__ == '__main__':
    print("🚀 Flask server starting on http://localhost:5050")
    app.run(port=5050)