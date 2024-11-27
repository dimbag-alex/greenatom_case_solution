from sqlalchemy.orm import Session
from models import Organization, Storage, OrgStorageEdge, StorageEdge
from schemas import OrganizationCreate, StorageCreate, OrgStorageEdgeCreate, StorageEdgeCreate



def create_organization(db: Session, org: OrganizationCreate):
    db_org = Organization(**org.dict())
    db.add(db_org)
    db.commit()
    db.refresh(db_org)
    return db_org



def create_storage(db: Session, storage: StorageCreate):
    db_storage = Storage(**storage.dict())
    db.add(db_storage)
    db.commit()
    db.refresh(db_storage)
    return db_storage


def create_org_storage_edge(db: Session, edge: OrgStorageEdgeCreate):
    db_edge = OrgStorageEdge(**edge.dict())
    db.add(db_edge)
    db.commit()
    db.refresh(db_edge)
    return db_edge


def create_storage_edge(db: Session, edge: StorageEdgeCreate):
    db_edge = StorageEdge(**edge.dict())
    db.add(db_edge)
    db.commit()
    db.refresh(db_edge)
    return db_edge


def get_all_organizations(db: Session):
    return db.query(Organization).all()


def get_all_storages(db: Session):
    return db.query(Storage).all()


def get_all_edges(db: Session):
    org_storage_edges = db.query(OrgStorageEdge).all()
    storage_edges = db.query(StorageEdge).all()
    return org_storage_edges, storage_edges
