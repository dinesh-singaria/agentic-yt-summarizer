"use client";

import { useState } from "react";
import ReactMarkdown from "react-markdown";

type Chapter = {
  start: string;
  title: string;
};

type ResultType = {
  summary: string;
  chapters: Chapter[];
  keyframes: string[];
  audio: string[];
};

export default function HomePage() {
  const [videoUrl, setVideoUrl] = useState("");
  const [prompt, setPrompt] = useState("");
  const [result, setResult] = useState<ResultType | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch("/api/summarize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ videoUrl, prompt }),
      });

      if (!response.ok) throw new Error("API failed");

      const data: ResultType = await response.json();
      setResult(data);
    } catch (err) {
      setError("Something went wrong. Please try again.");
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-xl mx-auto bg-white p-6 rounded-xl shadow-md">
        <h1 className="text-2xl font-bold mb-6 text-center text-gray-900">
          🎥 VidAgent: Prompt-Based Agentic Multimodal Summarizer
        </h1>
        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="text"
            placeholder="Enter YouTube URL"
            value={videoUrl}
            onChange={(e) => setVideoUrl(e.target.value)}
            required
            className="w-full p-3 border border-gray-300 rounded-lg text-gray-800 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <input
            type="text"
            placeholder='Prompt (e.g., "Summarize like I’m 10")'
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            className="w-full p-3 border border-gray-300 rounded-lg text-gray-800 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            type="submit"
            disabled={loading}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 w-full"
          >
            {loading ? "Summarizing..." : "Generate Summary"}
          </button>
        </form>

        {error && <p className="text-red-500 mt-4">{error}</p>}

        {result && (
          <div className="mt-6 space-y-6 text-gray-800">
            <div>
              {result?.summary && (
                <div className="prose prose-sm text-gray-800">
                  <ReactMarkdown>{result.summary}</ReactMarkdown>
                </div>
              )}
            </div>

            <div>
              <h3 className="font-medium text-gray-800">📌 Chapters:</h3>
              <ul className="list-disc list-inside text-gray-700">
                {result.chapters.map((chap, idx) => (
                  <li key={idx}>
                    [{chap.start}] {chap.title}
                  </li>
                ))}
              </ul>
            </div>

            <div>
              <h3 className="font-medium text-gray-800">🖼️ Keyframes:</h3>
              <div className="flex flex-wrap gap-2">
                {result.keyframes.map((url, idx) => (
                  <img
                    key={idx}
                    src={url}
                    alt={`Keyframe ${idx}`}
                    className="w-24 rounded border"
                  />
                ))}
              </div>
            </div>

            <div>
              <h3 className="font-medium text-gray-800">🔊 Audio Emotions:</h3>
              <ul className="list-disc list-inside text-gray-700">
                {result.audio.map((emotion, idx) => (
                  <li key={idx}>{emotion}</li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
