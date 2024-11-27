from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from graph_utils import distribute_waste, build_graph
from crud import get_all_organizations, get_all_storages, get_all_edges

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/run")
def run_distribution(db: Session = Depends(get_db)):
    # organizations = get_all_organizations(db)
    # storages = get_all_storages(db)
    # org_storage_edges, storage_edges = get_all_edges(db)

    steps = " ".join(distribute_waste(db=db, G=build_graph(db=db)))
    print(steps)
    return {"message": "Distribution completed", "steps": f'{steps}'}
