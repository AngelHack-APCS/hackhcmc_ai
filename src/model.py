import os
from llama_index.llms.openai import OpenAI
from llama_index.llms.groq import Groq
from dotenv import load_dotenv

load_dotenv(override=True)

def load_model(model_providder, model_name):
    if model_providder == "openai":
        
        llm = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"), model=model_name)
    elif model_providder == "groq":
        llm = Groq(api_key=os.environ.get("GROQ_API_KEY"), model=model_name)
    else:
        raise ValueError("Model provider must be either 'openai' or 'groq'")
    return llm
    
    