import os
from dotenv import load_dotenv
# from openai import OpenAI
from groq import Groq
import asyncio

load_dotenv(override=True)


def get_transcript(audio_path: str):
    # client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    with open(audio_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-large-v3", file=audio_file, language="vi" #, timestamp_granularities=["segment"]
        )
        return transcription.text

async def aget_transcript(file_path):
    transcription = await asyncio.to_thread(get_transcript, file_path)
    return transcription