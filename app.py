
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controller.prompt_controller import PromptController
from dotenv import load_dotenv

app = FastAPI()
promptController = PromptController()
load_dotenv()

app.include_router(promptController.router)
origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def health():
    return {"message": "Hello World"}
