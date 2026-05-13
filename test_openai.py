from openai import OpenAI
from src.config.settings import settings

client = OpenAI(api_key=settings.openai_api_key)

response = client.chat.completions.create(
    model=settings.openai_model,
    messages=[
        {"role": "user", "content": "Say: OpenAI API setup is working."}
    ]
)

print(response.choices[0].message.content)