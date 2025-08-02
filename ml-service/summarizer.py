import os
from dotenv import load_dotenv
from phi.agent import Agent, RunResponse
from phi.model.google import Gemini
from phi.tools.duckduckgo import DuckDuckGo

load_dotenv()

# Confirm the environment variable is loaded correctly
if not os.getenv("GEMINI_API_KEY"):
    raise RuntimeError(" GEMINI_API_KEY not found in environment")

# Create a phantom “agent” powered by Gemini 2.0 Flash Exp
agent = Agent(
    name="SummarizerAgent",
    model=Gemini(id="gemini-2.0-flash-exp"),
    tools=[DuckDuckGo()],
    markdown=True  # summaries prefer plain text
)

def summarize(transcript: str, prompt: str) -> str:
    """Run the summarization prompt through the Gemini agent."""
    full_prompt = f"{prompt.strip()}\n\nTranscript:\n{transcript.strip()}"
    run: RunResponse = agent.run(full_prompt)
    return run.content