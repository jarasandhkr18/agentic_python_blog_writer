import google.generativeai as genai
import os
import time
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

last_call_time = 0

def call_gemini(prompt: str, retries=5, cooldown=35) -> str:
    global last_call_time
    model = genai.GenerativeModel("models/gemini-1.5-pro-latest")

    for attempt in range(retries):
        # ⏳ Wait if needed (Gemini allows only 2 calls/min)
        elapsed = time.time() - last_call_time
        if elapsed < cooldown:
            wait = cooldown - elapsed
            print(f"⏸️ Waiting {int(wait)} seconds to respect Gemini rate limits...")
            time.sleep(wait)

        try:
            response = model.generate_content(prompt)
            last_call_time = time.time()
            return response.text
        except Exception as e:
            print(f"❌ Gemini SDK Error: {e}")
            if attempt < retries - 1:
                print(f"🔁 Retrying after {cooldown} seconds...")
                time.sleep(cooldown)
            else:
                return "Content could not be generated due to Gemini API rate limit. Try again after a few minutes."

