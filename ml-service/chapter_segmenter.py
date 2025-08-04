import re
import os
from phi.agent import Agent, RunResponse
from phi.model.google import Gemini

# Gemini agent for segmentation
segmenter_agent = Agent(
    name="ChapterSegmenter",
    model=Gemini(id="gemini-2.0-flash-exp"),
    markdown=True
)

def segment_into_chapters(transcript: str) -> str:
    prompt = """
You are a helpful assistant that segments long YouTube transcripts into chapters.

Instructions:
1. Divide the transcript into 3–7 meaningful chapters.
2. For each chapter, provide:
   - Start timestamp (mm:ss)
   - Chapter title (5–8 words)
   - 1-line summary explaining what is covered

3. Ensure the timestamps are realistic and in mm:ss format.
4. Maintain clear formatting as shown below:

Example Output:
00:00 - Chapter Title Here  
Summary: Short sentence describing this chapter.

01:40 - Next Chapter Title  
Summary: Description of what is discussed.

Transcript:
""" + transcript

    run: RunResponse = segmenter_agent.run(prompt)
    return run.content


def parse_chapters(text: str):
    chapters = []
    lines = text.strip().splitlines()
    current_chapter = {}

    for line in lines:
        time_title_match = re.match(r"(\d{2}:\d{2}) - (.+)", line)
        if time_title_match:
            if current_chapter:
                chapters.append(current_chapter)
                current_chapter = {}
            current_chapter["start"] = time_title_match.group(1)
            current_chapter["title"] = time_title_match.group(2)
        elif line.startswith("Summary:") and current_chapter:
            current_chapter["summary"] = line.replace("Summary:", "").strip()

    if current_chapter:
        chapters.append(current_chapter)

    return chapters