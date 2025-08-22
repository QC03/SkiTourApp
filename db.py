import sqlite3
from sqlite3 import Connection

DB_FILE = "SkiTourApp.db"


def get_conn() -> Connection:
    conn = sqlite3.connect(DB_FILE)
    return conn


def init_db():
    conn = get_conn()
    cur = conn.cursor()

    # 고객 테이블
    cur.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL
    )
    """)

    # 강사 테이블
    cur.execute("""
    CREATE TABLE IF NOT EXISTS instructors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        can_ski INTEGER DEFAULT 1,
        can_snowboard INTEGER DEFAULT 1,
        can_teach_english INTEGER DEFAULT 0,
        active INTEGER DEFAULT 1
    )
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
        instructor_id INTEGER,
        FOREIGN KEY(customer_id) REFERENCES customers(id),
        FOREIGN KEY(instructor_id) REFERENCES instructors(id)
    )
    """)

    conn.commit()
    conn.close()


# ----- 고객 관련 -----
def add_customer(name, phone):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO customers (name, phone) VALUES (?, ?)", (name, phone))
    conn.commit()
    cid = cur.lastrowid
    conn.close()
    return cid


def find_customer(name, phone):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id FROM customers WHERE name=? AND phone=?", (name, phone))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None


# ----- 강사 관련 -----
def get_instructors():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, name, can_ski, can_snowboard, can_teach_english, active FROM instructors")
    rows = cur.fetchall()
    conn.close()
    return rows


def add_instructor(name, can_ski=1, can_snowboard=1, can_teach_english=0, active=1):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO instructors (name, can_ski, can_snowboard, can_teach_english, active)
        VALUES (?, ?, ?, ?, ?)""", (name, can_ski, can_snowboard, can_teach_english, active))
    conn.commit()
    conn.close()


def update_instructor(inst_id, name, can_ski, can_snowboard, can_teach_english, active):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        UPDATE instructors SET name=?, can_ski=?, can_snowboard=?, can_teach_english=?, active=?
        WHERE id=?""", (name, can_ski, can_snowboard, can_teach_english, active, inst_id))
    conn.commit()
    conn.close()


def delete_instructor(inst_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM instructors WHERE id=?", (inst_id,))
    conn.commit()
    conn.close()


# ----- 예약 관련 -----
def add_booking(customer_id, date, start_time, duration_minutes,
                lesson_type, level, people_count, memo, instructor_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO bookings
        (customer_id, date, start_time, duration_minutes, lesson_type, level, people_count, memo, instructor_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (customer_id, date, start_time, duration_minutes, lesson_type, level, people_count, memo, instructor_id))
    conn.commit()
    conn.close()


def get_bookings():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT b.id, c.name, c.phone, b.date, b.start_time, b.duration_minutes,
               b.lesson_type, b.level, b.people_count, b.memo,
               i.name
        FROM bookings b
        LEFT JOIN customers c ON b.customer_id = c.id
        LEFT JOIN instructors i ON b.instructor_id = i.id
    """)
    rows = cur.fetchall()
    conn.close()
    return rows


def update_booking(booking_id, customer_id, date, start_time, duration_minutes,
                   lesson_type, level, people_count, memo, instructor_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        UPDATE bookings
        SET customer_id=?, date=?, start_time=?, duration_minutes=?, lesson_type=?, level=?,
            people_count=?, memo=?, instructor_id=?
        WHERE id=?
    """, (customer_id, date, start_time, duration_minutes, lesson_type, level,
          people_count, memo, instructor_id, booking_id))
    conn.commit()
    conn.close()


def delete_booking(booking_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM bookings WHERE id=?", (booking_id,))
    conn.commit()
    conn.close()
