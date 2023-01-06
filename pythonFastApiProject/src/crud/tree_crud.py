from sqlalchemy.orm import Session
from src.schemas.tree_schema import *
from src import models
import boto3

BUCKET_NAME = "tree-project-bucket"


def get_tree(db: Session, tree_id: int):
    tree = db.query(models.TreeModel).filter(models.TreeModel.id == tree_id).first()
    return tree


def get_all_public_trees(db: Session):
    trees = db.query(models.TreeModel).filter(models.TreeModel.private == 'false', models.TreeModel.deleted == 'false').all()
    return trees


def get_users_trees(db: Session, owner_id: int):
    users_trees = db.query(models.TreeModel).filter(models.TreeModel.owner_id == owner_id, models.TreeModel.deleted == 'false').all()
    return users_trees


def create_user_tree(file, db: Session, tree: TreeCreate):
    # Upload file to aws
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(BUCKET_NAME)
    bucket.upload_fileobj(file.file, file.filename, ExtraArgs={"ACL": "public-read"})
    uploaded_file_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{file.filename}"
    tree.img = uploaded_file_url
    db.add(tree)
    db.commit()
    db.refresh(tree)
    return tree


def delete_user_tree(db: Session, tree: TreeBase):
    db.add(tree)
    db.commit()
    db.refresh(tree)
