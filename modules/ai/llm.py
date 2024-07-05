import requests
from openai import OpenAI
from openai.types.chat import ChatCompletion
import os
from dotenv import load_dotenv
load_dotenv()

openai = OpenAI(
    base_url=os.getenv("OPENAI_BASE_URL"),
    api_key=os.getenv("OPENAI_API_KEY")
)

def list_models() -> list[str]:
    return [model.id for model in openai.models.list().data]

def get_response(prompt: str, model: str = "") -> str:
    completion: ChatCompletion = openai.chat.completions.create(
        model=model if model else os.getenv("LLM_MODEL"),
        messages=[
            {"role": "user", "content": prompt}
        ],
        stream=False,
        max_tokens=250
    )
    return completion.choices[0].message.content
