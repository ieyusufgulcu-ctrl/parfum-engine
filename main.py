from fastapi import FastAPI
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
    result = generate_scent(data.dict())
    return result

@app.post("/debug")
def debug(data: BirthData):
    from kerykeion import AstrologicalSubject
    person = AstrologicalSubject(
        data.name, data.year, data.month, data.day,
        data.hour, data.minute, data.city, data.nation
    )
    houses = []
    try:
        for h in person.houses_list:
            houses.append(str(h))
    except:
        houses = ["houses_list failed"]
    
    mc_attrs = {}
    for attr in ["tenth_house", "mc", "midheaven", "medium_coeli"]:
        try:
            val = getattr(person, attr, "NOT_FOUND")
            mc_attrs[attr] = str(val)
        except Exception as e:
            mc_attrs[attr] = str(e)
    
    return {"houses": houses[:5], "mc_attrs": mc_attrs}
