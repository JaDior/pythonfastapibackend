from sqlalchemy.orm import Session
from src.schemas.tree_schema import *
from src import models


def get_trees(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.TreeModel).offset(skip).limit(limit).all()


def get_users_trees(db: Session, owner_id: int):
    users_trees = db.query(models.TreeModel).filter(models.TreeModel.owner_id == owner_id).all()
    return users_trees


def create_user_tree(db: Session, tree: TreeCreate, user_id: int):
    db_tree = models.TreeModel(**tree.dict(), owner_id=user_id)
    db.add(db_tree)
    db.commit()
    db.refresh(db_tree)
    return db_tree
