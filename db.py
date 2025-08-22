import sqlite3
from pathlib import Path

DB_FILE = Path("ski_lesson.db")

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    # 강사 테이블
    cur.execute("""
    CREATE TABLE IF NOT EXISTS instructors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        can_ski BOOLEAN DEFAULT 1,
        can_snowboard BOOLEAN DEFAULT 0,
        can_teach_english BOOLEAN DEFAULT 0,
        active BOOLEAN DEFAULT 1
    );
    """)

    # 고객 테이블
    cur.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT UNIQUE,
        email TEXT
    );
    """)

    # 예약 테이블
    cur.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        date TEXT NOT NULL,
        start_time TEXT NOT NULL,
        duration_minutes INTEGER NOT NULL,
        lesson_type TEXT,
        level TEXT,
        people_count INTEGER DEFAULT 1,
        memo TEXT,
        FOREIGN KEY(customer_id) REFERENCES customers(id)
    );
    """)

    # 배정 테이블
    cur.execute("""
    CREATE TABLE IF NOT EXISTS assignments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        booking_id INTEGER,
        instructor_id INTEGER,
        start_dt TEXT NOT NULL,
        end_dt TEXT NOT NULL,
        FOREIGN KEY(booking_id) REFERENCES bookings(id),
        FOREIGN KEY(instructor_id) REFERENCES instructors(id)
    );
    """)

    conn.commit()
    conn.close()
