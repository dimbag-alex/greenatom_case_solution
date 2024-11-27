from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from crud import create_storage, get_all_storages
from schemas import StorageCreate


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/add")
def add_storage(storage: StorageCreate, db: Session = Depends(get_db)):
    return create_storage(db, storage)


@router.get("/")
def get_storages(db: Session = Depends(get_db)):
    storages = get_all_storages(db)
    return [
        {
            "name": storage.name,
            "capacity": storage.capacity,
            "filled": storage.filled,
        }
        for storage in storages
    ]