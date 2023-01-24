from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from backend.conv_manager.question_answering import  chatbot_get_response

load_dotenv()
app = FastAPI()


class Message(BaseModel):
    input: str
    user: str
    output: str = None
@app.get("/")
def chatbot_version():

    return {
        "system": "chatbot para cursos de INICTEL",
        "version": "0.2"
    }
@app.post("/chatbot/")
def chatbot_response(message: Message):
    reposnse = chatbot_get_response(message.user, message.input)
    print(reposnse)
    message.output = "response"
    return message



