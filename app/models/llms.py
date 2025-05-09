import os
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI


def setup_groq():
    GROQ_API_KEY = os.getenv("GROQ_KEY")
    model_name = "llama-3.1-8b-instant"
    llm = ChatGroq(temperature=0, model_name=model_name, groq_api_key=GROQ_API_KEY)
    return llm


def setup_lm_studio():
    llm = ChatOpenAI(
        temperature=0.0,
        base_url=f"http://{os.getenv('HOST')}:1234/v1",
        api_key="not-needed",
    )
    return llm
