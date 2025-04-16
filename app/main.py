"""
Main application module for the Common Assessment Tool.
This module initializes the FastAPI application and includes all routers.
Handles database initialization and CORS middleware configuration.
"""

"Just For Testing"
from fastapi import FastAPI
from app import models
from app.database import engine
from app.clients.router import router as clients_router, model_router
from app.auth.router import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize database tables
models.Base.metadata.create_all(bind=engine)

# Create FastAPI application
app = FastAPI(
    title="Case Management API", description="API for managing client cases", version="1.0.0"
)

# Include routers
app.include_router(auth_router)
app.include_router(clients_router, prefix="/clients", tags=["Clients"])
app.include_router(model_router)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
    allow_credentials=True,
)


@app.on_event("startup")
async def show_routes_on_startup():
    print("✅ LOADED ROUTES:")
    for route in app.routes:
        print(f"  {route.path}")


# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check():
    """
    Health check endpoint for monitoring

    Returns:
        dict: Status message
    """
    return {"status": "ok", "version": app.version}


if __name__ == "__main__":
    import uvicorn

    # Get port from environment variable or default to 8000
    port = int(os.getenv("PORT", 8000))

    # Start the application with uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=os.getenv("ENVIRONMENT", "production").lower() == "development",
    )
