from google import genai
from google.genai import types


def generate_llm_message(llm_client, name: str, interest_areas: str) -> str:
    """
    Generate a personalized message for WhatsApp using Gemini LLM.
    """
    prompt = (
        f"Write a short and friendly WhatsApp message (under 50 words) "
        f"for a person named {name} who is interested in {interest_areas}. "
        f"The message should be about opportunities in international nursing careers. "
        f"It should be warm, engaging, and relevant, and should not include any greeting from an AI."
    )
    
    response = llm_client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=[prompt],
    config=types.GenerateContentConfig(
        max_output_tokens=150,
        temperature=0.1
    ))
    
    return response.text.strip()