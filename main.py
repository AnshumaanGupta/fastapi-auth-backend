from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os

from routes import auth

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Authentication Backend",
    description="Backend API for user authentication with Supabase",
    version="1.0.0"
)

# CORS configuration for React frontend
origins = [
    os.getenv("FRONTEND_URL", "http://localhost:3000"),
    "http://localhost:3000",
    "http://209.38.123.128",
    "https://209.38.123.128",
    # Add your production frontend domain here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include authentication routes
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])

@app.get("/")
async def root():
    return {"message": "Authentication Backend API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    # Production configuration
    uvicorn.run(
        app, 
        host="127.0.0.1",  # Only listen on localhost, Nginx will proxy
        port=8000,
        workers=1,
        log_level="info"
    )
