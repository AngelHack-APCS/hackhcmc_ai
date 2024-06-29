import os
from openai import AsyncOpenAI
from prompt import SYSTEM_PROMPT
import chainlit as cl
from llama_index.core.base.llms.types import ChatMessage
from src.stt import get_transcript
from src.model import load_model


settings = {
    "model": "gpt-3.5-turbo",
    "temperature": 0.7,
    "max_tokens": 500,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
}

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set(
        "message_history",
        [{"role": "system", "content": SYSTEM_PROMPT}],
    )
    cl.user_session.set("llm", load_model("openai", "gpt-3.5-turbo"))
    
    await cl.Message(content="Welcome back to Mr. Capybara!").send()


@cl.on_message
async def on_message(message: cl.Message):
    content = message.content
    llm = cl.user_session.get("llm")
    
    for element in message.elements:
        if element.mime == "audio/wav":
            new_element_path = element.path + ".wav"
            print(new_element_path)
            os.rename(element.path, new_element_path)
            transcript = await get_transcript(new_element_path)
            content += "\n You are given this audio transcript: " + transcript
    
    message_history = cl.user_session.get("message_history")
    message_history.append({"role": "user", "content": message.content})

    msg = cl.Message(content="")
    await msg.send()
    
    response = await llm.astream_chat([ChatMessage(**m) for m in message_history])
    async for res in response:
        msg.content = res.message.content
        await msg.update()
    
    message_history.append({"role": "assistant", "content": msg.content})
    await msg.update()