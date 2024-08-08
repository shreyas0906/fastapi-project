from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import src.models as models
from src.database import engine

from .routers import post, user, auth, vote

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = ["*"] # update this so that only the FE can communicate with the backend

app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
async def read_root():
    return {"Hello": "welcome to my api"}



