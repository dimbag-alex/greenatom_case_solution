# from database import SessionLocal
from data_generator import populate_data
# from graph_utils import build_graph, distribute_waste

# if __name__ == "__main__":
#     db = SessionLocal()
#     populate_data(db)
#     G = build_graph(db)
#     distribute_waste(db, G)
#     db.close()

from fastapi import FastAPI
from database import SessionLocal, init_db
from routers import organizations, storages, edges, distribution

# init_db()
# db = SessionLocal()
# populate_data(db)
# db.close()
app = FastAPI()

app.include_router(organizations.router, prefix="/organizations", tags=["Organizations"])
app.include_router(storages.router, prefix="/storages", tags=["Storages"])
app.include_router(edges.router, prefix="/edges", tags=["Edges"])
app.include_router(distribution.router, prefix="/distribution", tags=["Distribution"])
