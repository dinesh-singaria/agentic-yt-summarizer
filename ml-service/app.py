from flask_cors import CORS
from flask import Flask, request, jsonify

app = Flask(__name__)
CORS(app)

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    video_url = data.get('videoUrl')
    prompt = data.get('prompt')

    # Dummy response (we'll replace with ML logic later)
    return jsonify({
        "summary": f"Summary of {video_url} using prompt '{prompt}'",
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