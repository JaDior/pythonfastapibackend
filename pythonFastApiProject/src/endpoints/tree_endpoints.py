from typing import Optional

from fastapi import Depends, APIRouter, HTTPException, UploadFile, Form
from sqlalchemy.orm import Session
import src.models
import src.crud.tree_crud
from src.auth.auth import get_current_active_user
from src.schemas.tree_schema import Tree
from src.models import TreeModel
from src.database import SessionLocal
from src.schemas.user_schema import UserBase
from src.auth.auth import authenticate_user

tree_router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@tree_router.get("/users/trees/public", response_model=list[Tree])
async def get_all_public_trees(current_user: UserBase = Depends(get_current_active_user), db: Session = Depends(get_db)):
    trees = src.crud.tree_crud.get_all_public_trees(db=db)
    return trees


@tree_router.post("/user/trees/")
async def create_tree_for_user(
        file: UploadFile,
        private: Optional[bool] = Form(None),
        name: Optional[str] = Form(None),
        species: Optional[str] = Form(None),
        genus: Optional[str] = Form(None),
        current_user: UserBase = Depends(get_current_active_user),
        db: Session = Depends(get_db)
):
    db_tree = TreeModel(private=private, name=name, species=species, genus=genus, deleted=False,  owner_id=current_user.id)
    return src.crud.tree_crud.create_user_tree(file=file, db=db, tree=db_tree)


@tree_router.get("/user/trees/", response_model=list[Tree])
async def get_users_trees(current_user: UserBase = Depends(get_current_active_user), db: Session = Depends(get_db)):
    trees = src.crud.tree_crud.get_users_trees(db=db, owner_id=current_user.id)
    return trees


@tree_router.patch("/user/tree-delete")
async def delete_users_tree(tree_id: int = Form(), current_user: UserBase = Depends(get_current_active_user), db: Session = Depends(get_db)):
    tree = src.crud.tree_crud.get_tree(db=db, tree_id=tree_id)
    setattr(tree, "deleted", True)
    src.crud.tree_crud.delete_user_tree(db=db, tree=tree)
