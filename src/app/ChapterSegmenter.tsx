// src/components/ChapterSegmenter.jsx

import React, { useState } from "react";

// Helper to parse Gemini markdown output (if needed)
function parseGeminiOutputToChapters(geminiOutput) {
  const lines = geminiOutput.trim().split("\n");
  const parsed = [];

  for (let i = 0; i < lines.length; i += 2) {
    const line1 = lines[i];
    const line2 = lines[i + 1] || "";

    const match = line1.match(/^(\d{2}:\d{2}) - (.+)$/);
    if (match) {
      const [_, start, title] = match;
      const summary = line2.replace("Summary: ", "").trim();
      parsed.push({ start, title, summary });
    }
  }
  return parsed;
}

const ChapterSegmenter = () => {
  const [transcript, setTranscript] = useState("");
  const [chapters, setChapters] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChapterSegmentation = async () => {
    setLoading(true);
    setError("");

    try {
      const res = await fetch("http://localhost:5001/segment", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ transcript }),
      });

      const data = await res.json();

      // If Gemini returns markdown text, parse it:
      if (data.chapters) {
        setChapters(data.chapters); // Already structured
      } else if (data.content) {
        const parsed = parseGeminiOutputToChapters(data.content);
        setChapters(parsed);
      }
    } catch (err) {
      console.error(err);
      setError("Something went wrong while fetching chapters.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white shadow rounded">
      <h2 className="text-xl font-semibold text-gray-800 mb-4">
        Chapter Segmentation
      </h2>

      <textarea
        value={transcript}
        onChange={(e) => setTranscript(e.target.value)}
        className="w-full h-48 p-2 border rounded"
        placeholder="Paste transcript here..."
      ></textarea>

      <button
        onClick={handleChapterSegmentation}
        className="mt-3 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
      >
        Segment Chapters
      </button>

      {loading && <p className="text-blue-500 mt-2">Loading chapters...</p>}
      {error && <p className="text-red-500 mt-2">{error}</p>}

      {chapters.length > 0 && (
        <div className="mt-6">
          <h3 className="font-medium text-gray-800 text-lg mb-2">
            📌 Chapters:
          </h3>
          <ul className="list-disc list-inside text-gray-700 space-y-1">
            {chapters.map((chap, idx) => (
              <li key={idx} className="leading-relaxed">
                <strong>
                  [{chap.start}] {chap.title}
                </strong>
                <br />
                <span className="text-sm text-gray-600">{chap.summary}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default ChapterSegmenter;
