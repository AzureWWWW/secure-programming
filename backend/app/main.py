from fastapi import FastAPI
from database import init_db
from api.api_router import api_router

from fastapi.middleware.cors import CORSMiddleware # to enable CORS



# Initialize FastAPI app
app = FastAPI()

# allow requests from the frontend
origins = [
    "http://localhost:4200",]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        
    allow_credentials=True,       # Allow cookies or credentials if needed
    allow_methods=["*"],          # Allow all HTTP requests
    allow_headers=["*"],          # Allow all headers
)
# initialize database
init_db()

# Include API routes
app.include_router(api_router)