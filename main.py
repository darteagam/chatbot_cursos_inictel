from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import  Union
from backend.conv_manager.question_answering import  chatbot_get_response
from backend.main import CHATBOT
load_dotenv()
app = FastAPI()
chatbot = CHATBOT()

class Message(BaseModel):
    input: str
    user: str
    output: Union [str,None] = None

@app.get("/")
def chatbot_version():
    return {
        "system": "chatbot para cursos de INICTEL",
        "version": "0.2"
    }

@app.post("/chatbot/")
def chatbot_response(message: Message):
    response = chatbot.get_response(message.user, message.input)
    message.output = response
    return message


