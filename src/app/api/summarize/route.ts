import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
  const { videoUrl, prompt } = await req.json();

  try {
    const response = await fetch("http://localhost:5050/summarize", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ videoUrl, prompt }),
    });

    if (!response.ok) {
      return NextResponse.json({ error: "Python API error" }, { status: 500 });
    }

    const data = await response.json();
    return NextResponse.json(data); // Forward the exact response to frontend
  } catch (error) {
    console.error("Failed to reach Python backend:", error);
    return NextResponse.json(
      { error: "Connection to backend failed" },
      { status: 500 }
    );
  }
}
