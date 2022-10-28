from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
import src.models
import src.crud.tree_crud
from src.schemas.tree_schema import Tree, TreeCreate
from src.database import SessionLocal


tree_router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@tree_router.post("/users/{user_id}/trees/", response_model=Tree)
def create_tree_for_user(user_id: int, tree: TreeCreate, db: Session = Depends(get_db)):
    return src.crud.tree_crud.create_user_tree(db=db, tree=tree, user_id=user_id)


@tree_router.get("/trees/", response_model=list[Tree])
def read_trees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    trees = src.crud.tree_crud.get_trees(db, skip=skip, limit=limit)
    return trees
