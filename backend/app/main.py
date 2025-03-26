from fastapi import FastAPI
from database import init_db
from api.api_router import api_router

# Initialize FastAPI app
app = FastAPI()

# initialize database
init_db()

# Include API routes
app.include_router(api_router)