from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Organization, Storage
from schemas import OrganizationBase, StorageBase

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/organizations/")
def create_organization(org: OrganizationBase, db: Session = Depends(get_db)):
    db_org = Organization(name=org.name, waste=org.waste)
    db.add(db_org)
    db.commit()
    db.refresh(db_org)
    return db_org


@router.post("/storages/")
def create_storage(storage: StorageBase, db: Session = Depends(get_db)):
    db_storage = Storage(name=storage.name, capacity=storage.capacity, filled=storage.filled)
    db.add(db_storage)
    db.commit()
    db.refresh(db_storage)
    return db_storage
