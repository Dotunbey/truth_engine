from fastapi import APIRouter
from app.core.engine import TruthEngine
from app.models.edge import Edge

router = APIRouter()
engine = TruthEngine()


@router.post("/evaluate")
def evaluate(edge: Edge, inputs: dict):
    return engine.evaluate(edge, inputs)
