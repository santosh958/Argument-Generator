import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load the API key from .env file
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Configure the generative AI client
genai.configure(api_key=api_key)

# Create the model
model = genai.GenerativeModel("models/gemini-1.5-flash")

# Prompt to send
prompt = "Explain how AI works in a few words."

# Generate content
try:
    response = model.generate_content(prompt)
    print("🔎 Gemini Response:\n")
    print(response.text)
except Exception as e:
    print("🔥 Gemini API Error:", str(e))
