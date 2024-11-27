from sqlalchemy.orm import Session
from models import Organization, Storage, OrgStorageEdge, StorageEdge
import networkx as nx


def build_graph(db: Session):
    G = nx.Graph()

    storages = db.query(Storage).all()
    organizations = db.query(Organization).all()

    for storage in storages:
        G.add_node(storage.name, type="storage")

    for org in organizations:
        G.add_node(org.name, type="organization")

    org_edges = db.query(OrgStorageEdge).all()
    for edge in org_edges:
        G.add_edge(edge.org_name, edge.storage_name, weight=edge.distance)

    storage_edges = db.query(StorageEdge).all()
    for edge in storage_edges:
        G.add_edge(edge.from_node, edge.to_node, weight=edge.distance)

    return G


def distribute_waste(db: Session, G):
    steps = []
    organizations = db.query(Organization).all()
    storages = {s.name: s for s in db.query(Storage).all()}

    for org in organizations:
        for waste_type, amount in org.waste.items():
            while amount > 0:
                paths = nx.single_source_dijkstra(G, org.name)
                for storage_name, distance in paths[0].items():
                    if storage_name in storages:
                        storage = storages[storage_name]
                        if waste_type in storage.capacity and storage.capacity[waste_type] > storage.filled[waste_type]:
                            to_transfer = min(amount, storage.capacity[waste_type] - storage.filled[waste_type])
                            storage.filled[waste_type] += to_transfer
                            amount -= to_transfer
                            
                            db.query(Storage).filter(Storage.name == storage_name).update(
                                {Storage.filled: storage.filled}, synchronize_session=False
                            )
                            db.commit()  # изменения в базе данных
                            
                            steps.append(f"Организация {org.name} отправила {to_transfer} {waste_type} в {storage_name}.\n")
                            break
                else:
                    raise Exception(f"Не удалось распределить все отходы для {org.name}.")
        org.waste = {w: 0 for w in org.waste.keys()}
    
    db.commit()
    return steps

