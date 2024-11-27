from sqlalchemy import Column, Integer, String, JSON, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    waste = Column(JSON, nullable=False)
    # {"пластик": 10, "стекло": 50}


class Storage(Base):
    __tablename__ = "storages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    capacity = Column(JSON, nullable=False)
    filled = Column(JSON, nullable=False)


class StorageEdge(Base):
    __tablename__ = "storage_edges"

    id = Column(Integer, primary_key=True, index=True)
    from_node = Column(String, nullable=False)
    to_node = Column(String, nullable=False)
    distance = Column(Float, nullable=False)


class OrgStorageEdge(Base):
    __tablename__ = "org_storage_edges"

    id = Column(Integer, primary_key=True, index=True)
    org_name = Column(String, nullable=False)
    storage_name = Column(String, nullable=False)
    distance = Column(Float, nullable=False)
