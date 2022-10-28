from pydantic import BaseModel


class TreeBase(BaseModel):
    name: str
    species: str
    genus: str
    img: str


class TreeCreate(TreeBase):
    pass


class Tree(TreeBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
