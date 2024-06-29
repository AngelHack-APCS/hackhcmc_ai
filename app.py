import os
import shutil
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from src.stt import get_transcript
from fastapi import FastAPI, File, UploadFile
from chainlit.auth import create_jwt
from chainlit.user import User
from chainlit.utils import mount_chainlit
from src.suggest_task import get_suggestions
from chainlit.context import init_http_context
import chainlit as cl

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/custom-auth")
async def custom_auth():
    # Verify the user's identity with custom logic.
    token = create_jwt(User(identifier="Test User"))
    return JSONResponse({"token": token})

@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...)):
    try:
        # Save the uploaded file temporarily
        file_location = f"temp/{file.filename}"
        os.makedirs(os.path.dirname(file_location), exist_ok=True)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        
        # Get the transcript
        transcript = get_transcript(file_location)
        # Delete the temporary file
        os.remove(file_location)
        
        return JSONResponse(content={"transcript": transcript}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/suggest")
async def get_suggestions_from_chainlit():
    init_http_context()
    message_history = cl.user_session.get("message_history")
    if not message_history:
        message_history = []
    output = await get_suggestions(message_history)
    return output
    


mount_chainlit(app=app, target="cl_app.py", path="/chainlit")


