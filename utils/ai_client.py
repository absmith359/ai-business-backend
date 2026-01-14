import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def generate_ai_response(context: str, message: str):
    prompt = f"""
You are an AI assistant for a business. Use ONLY the context below to answer.

CONTEXT:
{context}

USER MESSAGE:
{message}

If the answer is not in the context, say: 'I’m not sure, let me connect you with a representative.'
"""

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful business assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message["content"]