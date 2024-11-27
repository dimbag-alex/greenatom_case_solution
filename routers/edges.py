from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from crud import create_org_storage_edge, create_storage_edge
from schemas import OrgStorageEdgeCreate, StorageEdgeCreate
from models import OrgStorageEdge, StorageEdge

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Добавление маршрута организация-хранилище
@router.post("/org-storage/add")
def add_org_storage_edge(edge: OrgStorageEdgeCreate,
                         db: Session = Depends(get_db)):
    return create_org_storage_edge(db, edge)


# Добавление маршрута хранилище-хранилище
@router.post("/storage-storage/add")
def add_storage_edge(edge: StorageEdgeCreate, db: Session = Depends(get_db)):
    return create_storage_edge(db, edge)


@router.get("/org-storage")
def get_org_storage_edges(db: Session = Depends(get_db)):
    org_storage_edges = db.query(OrgStorageEdge).all()
    return [
        {
            "org_name": edge.org_name,
            "storage_name": edge.storage_name,
            "distance": edge.distance,
        }
        for edge in org_storage_edges
    ]


@router.get("/storage-storage")
def get_storage_edges(db: Session = Depends(get_db)):
    storage_edges = db.query(StorageEdge).all()
    return [
        {
            "from_node": edge.from_node,
            "to_node": edge.to_node,
            "distance": edge.distance,
        }
        for edge in storage_edges
    ]
