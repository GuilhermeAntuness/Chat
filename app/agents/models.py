import os

from langchain_groq import ChatGroq
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


llm_groq = ChatGroq(
    api_key=key_grok,
    model_name="llama3-70b-8192",
    temperature=0.7
)