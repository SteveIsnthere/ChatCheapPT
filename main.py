from fastapi import FastAPI
from fastapi import Body
import asyncio
from chat import get_chat_response, close_chat

app = FastAPI()

processing_lock = asyncio.Lock()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/get_response")
async def get_response(prompt: str = Body(...)):
    async with processing_lock:
        return get_chat_response(prompt)
