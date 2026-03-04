import sqlite3
import os

def get_db_path():
    app_data = os.getenv('LOCALAPPDATA')
    db_dir = os.path.join(app_data, 'AstroCategorizer')
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
    return os.path.join(db_dir, 'astro_data.db')

DB_PATH = get_db_path()

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT UNIQUE,
            filename TEXT,
            type TEXT DEFAULT 'Uncategorized',
            focal_length REAL DEFAULT 0.0,
            focal_category TEXT DEFAULT 'Unknown',
            description TEXT DEFAULT ''
        )
    """)
    conn.commit()
    conn.close()

def add_image(path):
    conn = get_connection()
    cursor = conn.cursor()
    filename = os.path.basename(path)
    try:
        cursor.execute("INSERT INTO images (path, filename) VALUES (?, ?)", (path, filename))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        # Image already exists
        cursor.execute("SELECT id FROM images WHERE path=?", (path,))
        row = cursor.fetchone()
        return row[0] if row else None
    finally:
        conn.close()

def get_all_images():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM images")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def update_image(img_id, img_type, focal_length, focal_category, description):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE images 
        SET type=?, focal_length=?, focal_category=?, description=?
        WHERE id=?
    """, (img_type, focal_length, focal_category, description, img_id))
    conn.commit()
    conn.close()

def delete_image(img_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM images WHERE id=?", (img_id,))
    conn.commit()
    conn.close()
