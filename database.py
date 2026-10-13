import sqlite3
import os
from typing import List, Dict, Optional, Any
from config import Config
from security import hash_password

def get_db_connection():
    """Returns a SQLite connection with dict-like row access."""
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    """Initializes tables and creates initial seed data if not present."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        full_name TEXT,
        phone_number TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Pets Table (Full Pet Profile with Health & Emergency info)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        species TEXT NOT NULL,          -- 'Kucing', 'Anjing', 'Arnab', etc.
        breed TEXT,                     -- cth: 'Domestic Shorthair / Kampung', 'British Shorthair', 'Golden Retriever'
        age_years INTEGER DEFAULT 0,
        age_months INTEGER DEFAULT 0,
        weight_kg REAL DEFAULT 0.0,
        gender TEXT DEFAULT 'Jantan',   -- 'Jantan', 'Betina', 'Jantan (Kembiri)', 'Betina (Mandul)'
        is_neutered INTEGER DEFAULT 0,  -- 1 = Ya, 0 = Tidak
        allergies TEXT,                 -- cth: 'Ayam, Gandum'
        medical_history TEXT,           -- cth: 'Pernah kena batu karang 2024'
        emergency_notes TEXT,           -- cth: 'Takut bunyi petir, cirit jika minum susu lembu'
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    # Chat Messages Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        pet_id INTEGER,
        sender TEXT NOT NULL,           -- 'user' atau 'bot'
        message TEXT NOT NULL,
        is_emergency INTEGER DEFAULT 0,
        triage_level TEXT DEFAULT 'INFO',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (pet_id) REFERENCES pets(id) ON DELETE SET NULL
    )
    """)

    # Emergency Events Log
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS emergency_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        pet_id INTEGER,
        trigger_reason TEXT NOT NULL,
        location_lat REAL,
        location_lng REAL,
        nearest_clinic_name TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()

    # Check if demo user exists, if not create demo user + sample pets
    cursor.execute("SELECT id FROM users WHERE username = ?", ('demo_malaysia',))
    demo_user = cursor.fetchone()
    if not demo_user:
        hashed = hash_password("demo12345")
        cursor.execute("""
        INSERT INTO users (username, email, password_hash, full_name, phone_number)
        VALUES (?, ?, ?, ?, ?)
        """, ('demo_malaysia', 'demo@petcare.my', hashed, 'Ahmad Faizal', '+60123456789'))
        user_id = cursor.lastrowid

        # Insert 2 sample Malaysian pets
        cursor.execute("""
        INSERT INTO pets (user_id, name, species, breed, age_years, age_months, weight_kg, gender, is_neutered, allergies, medical_history, emergency_notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id, 'Oyen', 'Kucing', 'Domestic Shorthair (Kucing Kampung)',
            2, 4, 3.8, 'Jantan (Kembiri)', 1,
            'Alahan ubat antibiotik amoxicillin',
            'Pernah rawatan kutu telinga (ear mites)',
            'Sensitif pada perubahan pasir najis, takut bunyi mercun'
        ))

        cursor.execute("""
        INSERT INTO pets (user_id, name, species, breed, age_years, age_months, weight_kg, gender, is_neutered, allergies, medical_history, emergency_notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id, 'Comel', 'Kucing', 'British Shorthair Mix',
            1, 2, 3.2, 'Betina (Mandul)', 1,
            'Tiada alahan diketahui',
            'Lengkap vaksin teras (Tricat)',
            'Mudah panik bila dimasukkan ke dalam sangkar pembawa'
        ))

        conn.commit()

    conn.close()

# --- USER OPERATIONS ---
def create_user(username: str, email: str, password_hash: str, full_name: str = "", phone_number: str = "") -> Optional[int]:
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO users (username, email, password_hash, full_name, phone_number)
        VALUES (?, ?, ?, ?, ?)
        """, (username.lower().strip(), email.lower().strip(), password_hash, full_name.strip(), phone_number.strip()))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def get_user_by_username_or_email(identifier: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM users WHERE LOWER(username) = LOWER(?) OR LOWER(email) = LOWER(?)
    """, (identifier.strip(), identifier.strip()))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email, full_name, phone_number, created_at FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

# --- PET CRUD OPERATIONS ---
def create_pet(user_id: int, data: Dict[str, Any]) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO pets (
        user_id, name, species, breed, age_years, age_months,
        weight_kg, gender, is_neutered, allergies, medical_history, emergency_notes
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        data.get('name', '').strip(),
        data.get('species', 'Kucing').strip(),
        data.get('breed', '').strip(),
        int(data.get('age_years', 0) or 0),
        int(data.get('age_months', 0) or 0),
        float(data.get('weight_kg', 0.0) or 0.0),
        data.get('gender', 'Jantan'),
        1 if data.get('is_neutered') else 0,
        data.get('allergies', '').strip(),
        data.get('medical_history', '').strip(),
        data.get('emergency_notes', '').strip()
    ))
    pet_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return pet_id

def get_user_pets(user_id: int) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM pets WHERE user_id = ? ORDER BY id ASC
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_pet_by_id(pet_id: int, user_id: int) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM pets WHERE id = ? AND user_id = ?
    """, (pet_id, user_id))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def update_pet(pet_id: int, user_id: int, data: Dict[str, Any]) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE pets SET
        name = ?, species = ?, breed = ?, age_years = ?, age_months = ?,
        weight_kg = ?, gender = ?, is_neutered = ?, allergies = ?,
        medical_history = ?, emergency_notes = ?, updated_at = CURRENT_TIMESTAMP
    WHERE id = ? AND user_id = ?
    """, (
        data.get('name', '').strip(),
        data.get('species', 'Kucing').strip(),
        data.get('breed', '').strip(),
        int(data.get('age_years', 0) or 0),
        int(data.get('age_months', 0) or 0),
        float(data.get('weight_kg', 0.0) or 0.0),
        data.get('gender', 'Jantan'),
        1 if data.get('is_neutered') else 0,
        data.get('allergies', '').strip(),
        data.get('medical_history', '').strip(),
        data.get('emergency_notes', '').strip(),
        pet_id,
        user_id
    ))
    updated = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return updated

def delete_pet(pet_id: int, user_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pets WHERE id = ? AND user_id = ?", (pet_id, user_id))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted

# --- CHAT & LOGS ---
def save_chat_message(user_id: int, pet_id: Optional[int], sender: str, message: str, is_emergency: bool = False, triage_level: str = 'INFO'):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO chat_messages (user_id, pet_id, sender, message, is_emergency, triage_level)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, pet_id, sender, message, 1 if is_emergency else 0, triage_level))
    conn.commit()
    conn.close()

def get_chat_history(user_id: int, pet_id: Optional[int] = None, limit: int = 50) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    if pet_id:
        cursor.execute("""
        SELECT * FROM chat_messages 
        WHERE user_id = ? AND pet_id = ? 
        ORDER BY id DESC LIMIT ?
        """, (user_id, pet_id, limit))
    else:
        cursor.execute("""
        SELECT * FROM chat_messages 
        WHERE user_id = ? 
        ORDER BY id DESC LIMIT ?
        """, (user_id, limit))
    rows = cursor.fetchall()
    conn.close()
    # Reverse so oldest first
    return [dict(r) for r in reversed(rows)]
