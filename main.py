from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager
from app.api.v1.routes import customer_routes, order_routes
from app.api.core.config import settings, logger  # Import logger
from app.api.core.database import initialize_database

@asynccontextmanager
async def lifespan(app: FastAPI):
    mongodb_client = AsyncIOMotorClient(settings.mongodb_url)
    app.mongodb = mongodb_client[settings.mongodb_db]
    logger.info("Connected to MongoDB!")

    await initialize_database()
    yield

    await mongodb_client.close()
    logger.info("Closed MongoDB connection!")

app = FastAPI(
    title="Customer Order API",
    description="A simple API for managing customers and orders",
    version="1.0.0",
    lifespan=lifespan,
)

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(customer_routes.router, prefix="/api/v1")
app.include_router(order_routes.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to the Customer Order API"}
