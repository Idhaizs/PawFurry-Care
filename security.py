import time
import re
import html
from functools import wraps
from typing import Dict, Tuple, Optional
import bcrypt
import jwt
from flask import request, jsonify, g
from config import Config

# --- PASSWORD HASHING (BCRYPT) ---
def hash_password(password: str) -> str:
    """Hashes a plain password with a secure bcrypt salt."""
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against the stored bcrypt hash."""
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False

# --- JWT TOKENS ---
def generate_jwt_token(user_id: int, username: str, email: str) -> str:
    """Generates an expiration-backed JWT token for authenticated sessions."""
    payload = {
        'sub': user_id,
        'username': username,
        'email': email,
        'iat': int(time.time()),
        'exp': int(time.time() + (Config.JWT_EXPIRATION_HOURS * 3600))
    }
    return jwt.encode(payload, Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM)

def decode_jwt_token(token: str) -> Optional[dict]:
    """Decodes and validates JWT token expiration and signature."""
    try:
        payload = jwt.decode(token, Config.JWT_SECRET, algorithms=[Config.JWT_ALGORITHM])
        return payload
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None

# --- AUTHENTICATION DECORATOR ---
def token_required(f):
    """Protects endpoints by verifying Bearer token in Authorization header."""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', None)
        if not auth_header:
            return jsonify({'success': False, 'error': 'Token pengesahan (Authorization header) diperlukan.'}), 401
        
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return jsonify({'success': False, 'error': 'Format token tidak sah. Guna format: Bearer <token>'}), 401
        
        token = parts[1]
        payload = decode_jwt_token(token)
        if not payload:
            return jsonify({'success': False, 'error': 'Sesi tamat atau token tidak sah. Sila log masuk semula.'}), 401
        
        # Attach user info to Flask globals
        g.current_user = {
            'id': payload['sub'],
            'username': payload['username'],
            'email': payload['email']
        }
        return f(*args, **kwargs)
    return decorated

def optional_token(f):
    """Extracts user token if present, but does not block guests."""
    @wraps(f)
    def decorated(*args, **kwargs):
        g.current_user = None
        auth_header = request.headers.get('Authorization', None)
        if auth_header:
            parts = auth_header.split()
            if len(parts) == 2 and parts[0].lower() == 'bearer':
                payload = decode_jwt_token(parts[1])
                if payload:
                    g.current_user = {
                        'id': payload['sub'],
                        'username': payload['username'],
                        'email': payload['email']
                    }
        return f(*args, **kwargs)
    return decorated

# --- RATE LIMITER (SLIDING WINDOW MEMORY CACHE) ---
class RateLimiter:
    """In-memory rate limiter tracking IP request timestamps to protect against brute-force and DDoS."""
    def __init__(self):
        self._requests: Dict[str, list] = {}

    def is_allowed(self, key: str, max_requests: int, window_seconds: int) -> Tuple[bool, int]:
        now = time.time()
        timestamps = self._requests.get(key, [])
        
        # Clean timestamps older than the window
        valid_timestamps = [ts for ts in timestamps if now - ts < window_seconds]
        
        if len(valid_timestamps) >= max_requests:
            remaining_wait = int(window_seconds - (now - valid_timestamps[0]))
            self._requests[key] = valid_timestamps
            return False, max(remaining_wait, 1)
        
        valid_timestamps.append(now)
        self._requests[key] = valid_timestamps
        return True, 0

rate_limiter = RateLimiter()

def rate_limit(limit_tuple: Tuple[int, int]):
    """Decorator to apply rate limits per client IP."""
    max_reqs, window_secs = limit_tuple
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            ip = request.headers.get('X-Forwarded-For', request.remote_addr) or '127.0.0.1'
            key = f"{ip}:{request.endpoint or f.__name__}"
            allowed, wait_seconds = rate_limiter.is_allowed(key, max_reqs, window_secs)
            if not allowed:
                return jsonify({
                    'success': False,
                    'error': f'Terlalu banyak percubaan. Sila tunggu {wait_seconds} saat sebelum cuba lagi.'
                }), 429
            return f(*args, **kwargs)
        return wrapped
    return decorator

# --- INPUT SANITIZATION & VALIDATION ---
def sanitize_text(text: Optional[str], max_length: int = 2000) -> str:
    """Escapes HTML entities and trims whitespace to prevent Cross-Site Scripting (XSS)."""
    if not text:
        return ""
    # Strip dangerous HTML tags
    cleaned = html.escape(str(text).strip())
    # Enforce reasonable length
    return cleaned[:max_length]

def validate_email(email: str) -> bool:
    """Validates email format using standard regex."""
    if not email:
        return False
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(pattern, email.strip()))

def validate_password_strength(password: str) -> Tuple[bool, str]:
    """Ensures password meets standard security strength (minimum 6 chars)."""
    if not password or len(password) < 6:
        return False, "Kata laluan mestilah sekurang-kurangnya 6 aksara."
    return True, ""

# --- SECURITY HEADERS MIDDLEWARE ---
def apply_security_headers(response):
    """Injects industry-standard HTTP security headers into every response."""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
        "style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com https://fonts.googleapis.com; "
        "font-src 'self' https://cdnjs.cloudflare.com https://fonts.gstatic.com; "
        "img-src 'self' data: https:; "
        "connect-src 'self';"
    )
    return response
