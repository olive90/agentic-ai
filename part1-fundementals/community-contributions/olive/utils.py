from google import genai
from groq import Groq

def optimizer(api_key, message):
    genai_client = genai.Client(api_key=api_key)

    messages = [{"role": "user", "content": message}]

    # Convert OpenAI-style messages to Gemini format
    system_prompt = ""
    conversation = []

    for msg in messages:
        if msg["role"] == "system":
            system_prompt = msg["content"]
        elif msg["role"] == "user":
            conversation.append(msg["content"])

    response = genai_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=conversation,
        config={"system_instruction": system_prompt} if system_prompt else None
    )

    ticket = response.text
    return ticket

def evaluator(api_key, message):
    groq_client = Groq(api_key=api_key)

    messages = [{"role": "user", "content": message}]

    # using groq
    groq_response = groq_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=messages
    )
    quality = groq_response.choices[0].message.content
    return quality