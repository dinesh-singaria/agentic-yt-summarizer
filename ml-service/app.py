from flask_cors import CORS
from flask import Flask, request, jsonify
from summarizer import summarize
from transcriber import get_transcript


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

    print("🚀 Done! Returning response.")

    return jsonify({
        "summary": summary,
        "chapters": [],
        "keyframes": [],
        "audio": []
    })

if __name__ == '__main__':
    app.run(port=5050)