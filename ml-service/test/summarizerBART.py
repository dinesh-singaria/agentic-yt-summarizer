from transformers import pipeline

# Load the BART summarizer once
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def generate_summary(transcript: str, user_prompt: str = "") -> str:
    # Sanitize input
    if not transcript:
        return "Transcript is empty."

    # Truncate to avoid max token limit for BART (1024 tokens ≈ 1024 characters here)
    if len(transcript) > 1024:
        transcript = transcript[:1024]

    # Combine user prompt and transcript
    if user_prompt.strip():
        full_input = f"{user_prompt.strip()}\n\n{transcript.strip()}"
    else:
        full_input = transcript.strip()

    try:
        result = summarizer(full_input, max_length=130, min_length=30, do_sample=False)
        return result[0]["summary_text"]
    except Exception as e:
        return f"❌ Error generating summary: {str(e)}"