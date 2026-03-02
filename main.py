from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from engine import generate_scent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class BirthData(BaseModel):
    name: str
    year: int
    month: int
    day: int
    hour: int
    minute: int
    city: str
    nation: str
    gender: str | None = None
    preferred_style: str | None = None
    disliked_tags: list[str] | None = []
    usage_time: str | None = None

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/calculate")
def calculate(data: BirthData):
    try:
        return generate_scent(data.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
