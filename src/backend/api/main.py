from fastapi import FastAPI

from db.session import metadata, engine
from api.issue import router
from fastapi.middleware.cors import CORSMiddleware


metadata.create_all(engine)


app = FastAPI()

origins = ["http://localhost:8000", "http://localhost:5173", "http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
