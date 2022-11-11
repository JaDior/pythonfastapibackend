from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
import src.models
import src.crud.tree_crud
from src.auth.auth import get_current_active_user
from src.schemas.tree_schema import Tree, TreeCreate
from src.database import SessionLocal
from src.schemas.user_schema import UserBase

tree_router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@tree_router.post("/user/trees/", response_model=Tree)
def create_tree_for_user(tree: TreeCreate, current_user: UserBase = Depends(get_current_active_user), db: Session = Depends(get_db)):
    return src.crud.tree_crud.create_user_tree(db=db, tree=tree, user_id=current_user.id)


@tree_router.get("/user/trees/", response_model=list[Tree])
async def get_users_trees(current_user: UserBase = Depends(get_current_active_user), db: Session = Depends(get_db)):
    trees = src.crud.tree_crud.get_users_trees(db=db, owner_id=current_user.id)
    return trees
