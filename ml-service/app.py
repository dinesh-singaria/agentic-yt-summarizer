from flask_cors import CORS
from flask import Flask, request, jsonify
from summarizer import generate_summary

app = Flask(__name__)
CORS(app)

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    video_url = data.get('videoUrl')
    prompt = data.get('prompt')

     # Dummy text for now (replace with Whisper later)
    transcript = "The video explains the lifecycle of a butterfly, starting from egg to caterpillar, then chrysalis and finally an adult butterfly."

    summary = generate_summary(transcript, prompt)


    # Dummy response (we'll replace with ML logic later)
    return jsonify({
        "summary": summary,
        "chapters": [
            {"start": "00:00", "title": "Intro"},
            {"start": "01:00", "title": "Main Ideas"},
            {"start": "02:30", "title": "Wrap Up"}
        ],
        "keyframes": [
            "https://via.placeholder.com/120x80?text=Frame1",
            "https://via.placeholder.com/120x80?text=Frame2"
        ],
        "audio": ["Happy", "Neutral"]
    })

if __name__ == '__main__':
    app.run(port=5050)