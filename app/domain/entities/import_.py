from sqlalchemy import Column, Integer, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Import(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    grupo = Column(
        str(50),
        nullable=False,
    )
    pais = Column(str(100), nullable=False)
    quantidade = Column(Float, nullable=False)
    valor = Column(Float, unique=True, nullable=False)
