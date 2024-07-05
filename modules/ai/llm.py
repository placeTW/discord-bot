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
    # TODO: use the OpenAI implementation
    # Should be compatible with Ollama soon: https://github.com/ollama/ollama/pull/5007
    # return openai.models.list().data
    URL = os.getenv("OPENAI_BASE_URL").replace('/v1', '') + "/api/tags"
    response = requests.get(URL)
    return [model['model'] for model in response.json()['models']]

def get_response(prompt: str, model: str = "") -> str:
    completion: ChatCompletion = openai.chat.completions.create(
        model=model or os.getenv("LLM_MODEL"),
        messages=[
            {"role": "user", "content": prompt}
        ],
        stream=False
    )
    return completion.choices[0].message.content
