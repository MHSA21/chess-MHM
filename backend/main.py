from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from stockfish import Stockfish
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STOCKFISH_PATH = os.getenv("STOCKFISH_PATH", "./stockfish")
stockfish = Stockfish(path=STOCKFISH_PATH)

class AnalyzeRequest(BaseModel):
    fen: str
    rating: int
    style: str

@app.post("/analyze")
def analyze_move(data: AnalyzeRequest):
    fen = data.fen
    rating = data.rating
    style = data.style

    if rating < 1000:
        skill = 1
        depth = 6
    elif rating < 1500:
        skill = 5
        depth = 8
    elif rating < 2000:
        skill = 10
        depth = 10
    elif rating < 2500:
        skill = 15
        depth = 14
    else:
        skill = 20
        depth = 18

    contempt = {
        "aggressive": 50,
        "defensive": -50,
        "balanced": 0
    }.get(style, 0)

    stockfish.update_engine_parameters({
        "Skill Level": skill,
        "Contempt": contempt
    })
    stockfish.set_depth(depth)
    stockfish.set_fen_position(fen)

    best_move = stockfish.get_best_move()
    return {"best_move": best_move}
