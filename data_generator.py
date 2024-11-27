from sqlalchemy.orm import Session
from database import SessionLocal, init_db
from models import Organization, Storage, StorageEdge, OrgStorageEdge


def populate_data(db: Session):


    # Добавление организаций
    organizations = [
        {"name": "ОО1", "waste": {"пластик": 10, "стекло": 50, "биоотходы": 50}},
        {"name": "ОО2", "waste": {"пластик": 60, "стекло": 20, "биоотходы": 50}},
    ]

    for org in organizations:
        db_org = Organization(name=org["name"], waste=org["waste"])
        db.add(db_org)

    # Добавление хранилищ
    storages = [
        {"name": "МНО1", "capacity": {"стекло": 300, "пластик": 100}, "filled": {"стекло": 0, "пластик": 0}},
        {"name": "МНО2", "capacity": {"пластик": 50, "биоотходы": 150}, "filled": {"пластик": 0, "биоотходы": 0}},
        {"name": "МНО3", "capacity": {"пластик": 10, "биоотходы": 250}, "filled": {"пластик": 0, "биоотходы": 0}},
        {"name": "МНО5", "capacity": {"стекло": 220, "биоотходы": 25}, "filled": {"стекло": 0, "биоотходы": 0}},
        {"name": "МНО6", "capacity": {"стекло": 100, "биоотходы": 150}, "filled": {"стекло": 0, "биоотходы": 0}},
        {"name": "МНО7", "capacity": {"пластик": 100, "биоотходы": 250}, "filled": {"пластик": 0, "биоотходы": 0}},
        {"name": "МНО8", "capacity": {"стекло": 35, "пластик": 25, "биоотходы": 52}, "filled": {"стекло": 0, "пластик": 0, "биоотходы": 0}},
        {"name": "МНО9", "capacity": {"пластик": 250, "биоотходы": 20}, "filled": {"пластик": 0, "биоотходы": 0}},
    ]

    for storage in storages:
        db_storage = Storage(name=storage["name"], capacity=storage["capacity"], filled=storage["filled"])
        db.add(db_storage)

    org_storage_edges = [
        {"org_name": "ОО1", "storage_name": "МНО1", "distance": 100},
        {"org_name": "ОО1", "storage_name": "МНО2", "distance": 50},
        {"org_name": "ОО1", "storage_name": "МНО3", "distance": 600},
        {"org_name": "ОО2", "storage_name": "МНО3", "distance": 50},
    ]

    for edge in org_storage_edges:
        db_edge = OrgStorageEdge(org_name=edge["org_name"], storage_name=edge["storage_name"], distance=edge["distance"])
        db.add(db_edge)

    storage_edges = [
        {"from_node": "МНО1", "to_node": "МНО8", "distance": 500},
        {"from_node": "МНО8", "to_node": "МНО9", "distance": 10},
        {"from_node": "МНО2", "to_node": "МНО5", "distance": 50},
        {"from_node": "МНО3", "to_node": "МНО7", "distance": 50},
        {"from_node": "МНО3", "to_node": "МНО6", "distance": 600},
    ]

    for edge in storage_edges:
        db_edge = StorageEdge(from_node=edge["from_node"], to_node=edge["to_node"], distance=edge["distance"])
        db.add(db_edge)

    db.commit()


if __name__ == "__main__":
    init_db()
    db = SessionLocal()
    populate_data(db)
    db.close()
