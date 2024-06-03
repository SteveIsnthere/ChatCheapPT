from fastapi import FastAPI
from fastapi import Body

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/get_response")
async def get_response(prompt: str = Body(...)):
    return {"response": "This is a response to the prompt: " + prompt}