from pydantic import BaseModel


class TreeBase(BaseModel):
    private: bool
    name: str
    species: str
    genus: str
    img: str


class TreeCreate(TreeBase):
    pass


class Tree(TreeBase):
    id: int
    deleted: bool
    owner_id: int

    class Config:
        orm_mode = True
