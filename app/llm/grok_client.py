import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROK_API_KEY")
URL = "https://api.x.ai/v1/chat/completions"


def generate(prompt: str):

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "Llama-3.1-8B",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(URL, headers=headers, json=data)
    print(response.json())
    return response.json()["choices"][0]["message"]["content"]