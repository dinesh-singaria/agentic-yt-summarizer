from summarizer import generate_summary

transcript = "This video explains how to use LangChain with Dash to build a custom LLM app that accepts user instructions and a YouTube link. It then summarizes the video content using the script."

prompt = "Summarize in key points"

summary = generate_summary(transcript, prompt)

print("🧠 Generated Summary:\n", summary)