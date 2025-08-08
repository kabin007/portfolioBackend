#!/usr/bin/env python3
"""
Script to run the Chat Application
"""
import uvicorn
import os
from app.config import settings


if __name__ == "__main__":
    # Get configuration from environment variables
    host = settings.host
    port = settings.port
    debug = settings.debug

    print(f"Starting Chat Application...")
    print(f"Server will be available at: http://{host}:{port}")
    print(f"API Documentation: http://{host}:{port}/docs")
    print(f"Debug mode: {debug}")

    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info" if debug else "warning"
    )
