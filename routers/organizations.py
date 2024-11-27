from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from crud import create_organization, get_all_organizations
from schemas import OrganizationCreate

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/add")
def add_organization(org: OrganizationCreate, db: Session = Depends(get_db)):
    return create_organization(db, org)


@router.get("/")
def get_organizations(db: Session = Depends(get_db)):
    organizations = get_all_organizations(db)
    return [{"name": org.name, "waste": org.waste} for org in organizations]
