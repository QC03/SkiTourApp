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


# CRUD
def get_instructors():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT id, name, can_ski, can_snowboard, can_teach_english, active FROM instructors")
    rows = cur.fetchall()
    conn.close()
    return rows

def add_instructor(name, can_ski=True, can_snowboard=False, can_teach_english=False, active=True):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO instructors (name, can_ski, can_snowboard, can_teach_english, active)
        VALUES (?, ?, ?, ?, ?)
    """, (name, int(can_ski), int(can_snowboard), int(can_teach_english), int(active)))
    conn.commit()
    conn.close()

def update_instructor(iid, name, can_ski, can_snowboard, can_teach_english, active):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        UPDATE instructors SET name=?, can_ski=?, can_snowboard=?, can_teach_english=?, active=?
        WHERE id=?
    """, (name, int(can_ski), int(can_snowboard), int(can_teach_english), int(active), iid))
    conn.commit()
    conn.close()

def delete_instructor(iid):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("DELETE FROM instructors WHERE id=?", (iid,))
    conn.commit()
    conn.close()