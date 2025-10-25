import os
import psycopg2

def get_connection():
    return psycopg2.connect(
        host=os.environ.get('DB_HOST'),
        database=os.environ.get('DB_NAME'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD')
    )

def get_users():
    conn = get_connection()
    cur = conn.cursor()

    # ensure table exists before select
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name TEXT UNIQUE
        );
    """)
    conn.commit()

    # select all users
    cur.execute("SELECT * FROM users;")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [{"id": r[0], "name": r[1]} for r in rows]

def add_user(name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name TEXT UNIQUE
        );
    """)
    cur.execute(
        "INSERT INTO users(name) VALUES (%s) ON CONFLICT (name) DO NOTHING;",
        (name,)
    )
    conn.commit()
    cur.close()
    conn.close()
