from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.database import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    disabled = Column(Boolean, default=False)

    trees = relationship("TreeModel", back_populates="owner")


class TreeModel(Base):
    __tablename__ = "trees"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    species = Column(String, index=True)
    genus = Column(String, index=True)
    img = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("UserModel", back_populates="trees")
