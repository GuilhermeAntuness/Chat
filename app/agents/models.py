import os

from groq import Groq
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

key_gemini = os.getenv("KEY_GEMINI")
key_grok = os.getenv("KEY_GROQ")

llm_gemini = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    api_key=key_gemini,
    temperature=1,

)


client = Groq(
    # This is the default and can be omitted
    api_key=os.getenv('KEY_GROQ'),
)