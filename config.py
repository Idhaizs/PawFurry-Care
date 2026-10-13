import os
from datetime import timedelta

class Config:
    # Security Secrets
    SECRET_KEY = os.environ.get("SECRET_KEY", "mypetcare-secret-key-malaysia-2026-prod-guard")
    JWT_SECRET = os.environ.get("JWT_SECRET", "jwt-super-secure-token-petcare-my-998811")
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRATION_HOURS = 72

    # Database Path
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATABASE_PATH = os.path.join(BASE_DIR, "petcare.db")

    # Rate Limiting Configurations (Requests, Seconds)
    RATE_LIMIT_LOGIN = (5, 60)      # Max 5 attempts per minute
    RATE_LIMIT_REGISTER = (3, 60)   # Max 3 attempts per minute
    RATE_LIMIT_CHAT = (30, 60)      # Max 30 messages per minute
    RATE_LIMIT_GENERAL = (100, 60)  # Max 100 general requests per minute

    # AI Integration
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

    # Security Settings
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
