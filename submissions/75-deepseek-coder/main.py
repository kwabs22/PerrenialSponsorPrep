"""DeepSeek Coder Demo"""
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("DEEPSEEK_API_KEY")

def code_complete(prompt):
    try:
        from openai import OpenAI
        if API_KEY:
            client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com")
            response = client.chat.completions.create(
                model="deepseek-coder",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
    except: pass
    return f"[Demo] Code for: {prompt}"

def main():
    print("DeepSeek Coder Demo")
    print(code_complete("Write a Python function for binary search"))

if __name__ == "__main__":
    main()
