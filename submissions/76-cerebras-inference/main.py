"""Cerebras Inference Demo"""
import os, time
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("CEREBRAS_API_KEY")

def fast_inference(prompt):
    try:
        from cerebras.cloud.sdk import Cerebras
        if API_KEY:
            client = Cerebras(api_key=API_KEY)
            start = time.time()
            response = client.chat.completions.create(
                model="llama3.1-8b",
                messages=[{"role": "user", "content": prompt}]
            )
            elapsed = time.time() - start
            return f"{response.choices[0].message.content}\n[{elapsed:.2f}s]"
    except: pass
    return f"[Demo] Ultra-fast response to: {prompt}"

def main():
    print("Cerebras Inference Demo")
    print(fast_inference("Explain quantum computing"))

if __name__ == "__main__":
    main()
