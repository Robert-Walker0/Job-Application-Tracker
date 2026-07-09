import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import initialize_project_databases
from routes.applications import router

FRONTEND_LOCAL_URL = "https://localhost:5173"
FRONTEND_REMOTE_URL = os.getenv("FRONTEND_REMOTE_URL", FRONTEND_LOCAL_URL)

@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_project_databases()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        FRONTEND_LOCAL_URL,
        FRONTEND_REMOTE_URL
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
