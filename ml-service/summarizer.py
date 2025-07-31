from transformers import pipeline

# Load the BART summarizer
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def generate_summary(text: str, user_prompt: str = "") -> str:
    """
    Summarizes the input text with an optional user prompt.

    Parameters:
        text (str): The input transcript to summarize
        user_prompt (str): A custom user prompt like 'Summarize like I’m 10'

    Returns:
        str: The personalized summary
    """
    # Truncate text if it's too long for BART
    if len(text) > 1024:
        text = text[:1024]

    summary = summarizer(text, max_length=130, min_length=30, do_sample=False)[0]['summary_text']

    if user_prompt:
        # Add personalization (simple prompt injection)
        summary = f"{user_prompt.strip().capitalize()}: {summary}"

    return summary