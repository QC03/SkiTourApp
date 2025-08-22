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
        phone TEXT,
        note TEXT
    )
    """)

    # 고객 테이블
    cur.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT
    )
    """)

    # 예약(강습) 테이블
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
        instructor_id INTEGER,
        FOREIGN KEY(customer_id) REFERENCES customers(id),
        FOREIGN KEY(instructor_id) REFERENCES instructors(id)
    )
    """)

    conn.commit()
    conn.close()


# Instructor CRUD
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


# Customer
def add_booking(customer_id, date, start_time, duration_minutes, lesson_type, level, people_count, memo, instructor_id):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO bookings (customer_id, date, start_time, duration_minutes, lesson_type, level, people_count, memo, instructor_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (customer_id, date, start_time, duration_minutes, lesson_type, level, people_count, memo, instructor_id))
    conn.commit()
    conn.close()

def get_bookings():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        SELECT b.id, c.name, c.phone, b.date, b.start_time, b.duration_minutes,
               b.lesson_type, b.level, b.people_count, b.memo, i.name
        FROM bookings b
        JOIN customers c ON b.customer_id = c.id
        LEFT JOIN instructors i ON b.instructor_id = i.id
    """)
    rows = cur.fetchall()
    conn.close()
    return rows