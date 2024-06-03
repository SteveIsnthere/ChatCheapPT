from fastapi import FastAPI
from fastapi import Body, Request
import asyncio
from chat import get_chat_response, close_chat

app = FastAPI()

processing_lock = asyncio.Lock()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/get_response")
async def get_response(request: Request):
    async with processing_lock:
        prompt = await request.body()
        prompt_str = prompt.decode('utf-8')
        return get_chat_response(prompt_str)
