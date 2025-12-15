"""xAI Grok Demo"""
import os, requests
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("XAI_API_KEY")

def chat(prompt):
    if not API_KEY:
        return f"[Demo] Grok response to: {prompt}"
    response = requests.post(
        "https://api.x.ai/v1/chat/completions",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"model": "grok-2-latest", "messages": [{"role": "user", "content": prompt}]}
    )
    return response.json()["choices"][0]["message"]["content"]

def main():
    print("xAI Grok Demo")
    print(chat("What's happening in AI today?"))

if __name__ == "__main__":
    main()
