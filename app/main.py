from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import logging
from app.database.db import create_tables, get_db
from app.routes import auth_routes
from app.models import user
import uvicorn


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Simple Auth API",
    description="An authorization endpoint",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_routes.router)


@app.on_event("startup")
async def startup_event():
    """Create database tables on startup"""
    logger.info("Creating database tables...")
    await create_tables()
    logger.info("Database tables created successfully")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Auth API",
        "version": "1.0.0",
        "docs": "/docs"
    }



@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running"}




if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
