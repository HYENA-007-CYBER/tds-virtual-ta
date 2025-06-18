from fastapi import FastAPI
from pydantic import BaseModel
from app.qa_engine import answer_question
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# CORS (helpful for frontend integration/testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    question: str
    image: str | None = None  # Optional image in base64

@app.post("/api/")
async def get_answer(request: QuestionRequest):
    try:
        response = answer_question(request.question, request.image)
        return response
    except Exception as e:
        return {
            "answer": "An error occurred while processing your request.",
            "links": [],
            "error": str(e)
        }

