import os
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path

# Load .env file from current folder
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("❌ OPENAI_API_KEY is missing in .env")

client = OpenAI(api_key=api_key)

def generate_summary(transcript: str, user_prompt: str = "") -> str:
    if not transcript.strip():
        return "Transcript is empty."

    prompt = f"{user_prompt.strip()}\n\nTranscript:\n{transcript.strip()}"

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes videos based on transcript and user prompts."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.5
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error with OpenAI API: {str(e)}"