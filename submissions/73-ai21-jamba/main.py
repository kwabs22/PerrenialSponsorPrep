"""AI21 Jamba Demo"""
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("AI21_API_KEY")

def chat(prompt):
    try:
        from ai21 import AI21Client
        if API_KEY:
            client = AI21Client(api_key=API_KEY)
            response = client.chat.completions.create(
                model="jamba-1.5-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
    except: pass
    return f"[Demo] Response to: {prompt}"

def main():
    print("AI21 Jamba Demo")
    print(chat("Explain hybrid SSM-Transformer architecture"))

if __name__ == "__main__":
    main()
