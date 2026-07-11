import os
from dotenv import load_dotenv
load_dotenv()

from origins import get_frontend_remote_origin
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import initialize_project_databases
from routes.applications import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_project_databases()
    yield

app = FastAPI(lifespan=lifespan)



app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        get_frontend_remote_origin()
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
