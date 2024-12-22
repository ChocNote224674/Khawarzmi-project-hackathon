# api.py
from fastapi import FastAPI
from pydantic import BaseModel
from agents import QuestionAskingAgent, MedicalReportAgent
from config import openai_api_key
from langchain.llms import OpenAI

app = FastAPI()

# Classe pour définir la structure de la requête
class QuestionRequest(BaseModel):
    questions: list
    responses: dict

# Créer une instance de LLM
llm = OpenAI(openai_api_key=openai_api_key)

@app.post("/ask_questions/")
def ask_questions(request: QuestionRequest):
    agent = QuestionAskingAgent(request.questions, llm)
    responses = agent.ask_questions()
    return {"responses": responses}

@app.post("/generate_report/")
def generate_report(request: QuestionRequest):
    agent = MedicalReportAgent(llm)
    report = agent.generate_report(request.responses)
    return {"report": report}
