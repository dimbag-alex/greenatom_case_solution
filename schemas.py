from pydantic import BaseModel
from typing import Dict


class OrganizationBase(BaseModel):
    name: str
    waste: Dict[str, int]


class OrganizationCreate(OrganizationBase):
    pass


class StorageBase(BaseModel):
    name: str
    capacity: Dict[str, int]
    filled: Dict[str, int]


class StorageCreate(StorageBase):
    pass


class EdgeBase(BaseModel):
    distance: float


class OrgStorageEdgeCreate(EdgeBase):
    org_name: str
    storage_name: str


class StorageEdgeCreate(EdgeBase):
    from_node: str
    to_node: str
