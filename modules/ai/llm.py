from openai import OpenAI
from openai.types.chat import ChatCompletion
import os
from dotenv import load_dotenv
load_dotenv()

openai = OpenAI(
    base_url=os.getenv("OPENAI_BASE_URL"),
    api_key=os.getenv("OPENAI_API_KEY")
)

def get_response(prompt: str) -> str:
    completion: ChatCompletion = openai.chat.completions.create(
        model=os.getenv("LLM_MODEL"),
        messages=[
            {"role": "user", "content": prompt}
        ],
        stream=False
    )
    return completion.choices[0].message.content
