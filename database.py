from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from models import Base

DATABASE_URL = "postgresql://postgres:postgres@localhost/greenatom_test"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    # удалить и создать заново тестовые данные
    print("Удалили все старое")
    Base.metadata.drop_all(bind=engine)
    print("Записали все новое")
    Base.metadata.create_all(bind=engine)

