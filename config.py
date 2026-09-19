import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URI = os.getenv("MONGO_URI")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret-key-change-in-production")
    
    # Increase token expiration to 24 hours (86400 seconds) for development
    JWT_ACCESS_TOKEN_EXPIRES = 86400
