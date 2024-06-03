from fastapi import FastAPI
from fastapi import Body, Request
import asyncio
from chat import get_chat_response, close_chat, get_chat_response_with_context
from pydantic import BaseModel

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


class PromptContext(BaseModel):
    prompt: str
    context: str


@app.post("/get_response_with_context")
async def get_response_with_context(data: PromptContext = Body(...)):
    prompt = data.prompt
    context = data.context

    async with processing_lock:
        res = get_chat_response_with_context(prompt, context)
        if res.endswith("\nReference files:\ncontext.txt"):
            res = res.replace("\nReference files:\ncontext.txt", "")
        return res
