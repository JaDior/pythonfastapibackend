from fastapi import Depends, FastAPI, HTTPException
import uvicorn
import src.models
import src.crud
from src.endpoints.tree_endpoints import tree_router
from src.endpoints.user_endpoints import user_router
from src.endpoints.auth_endpoints import auth_router
from src.database import SessionLocal, engine


app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(tree_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    src.models.Base.metadata.create_all(bind=engine)
