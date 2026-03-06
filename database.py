import sqlite3
import os
import json

def get_db_path():
    app_data = os.getenv('LOCALAPPDATA')
    if not app_data:
        app_data = os.path.expanduser('~')
    db_dir = os.path.join(app_data, 'AstroCategorizer')
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
    return os.path.join(db_dir, 'astro_data.db')

DB_PATH = get_db_path()

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Crea la tabella base
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
    
    # Migrazione sicura: aggiungi nuove colonne se mancanti
    new_columns = [
        ('title',            'TEXT DEFAULT ""'),
        ('ra',               'TEXT DEFAULT ""'),
        ('dec',              'TEXT DEFAULT ""'),
        ('constellation',    'TEXT DEFAULT ""'),
        ('equipment',        'TEXT DEFAULT ""'),
        ('integration_time', 'TEXT DEFAULT ""'),
        ('location',         'TEXT DEFAULT ""'),
        ('date_acquired',    'TEXT DEFAULT ""'),
        ('tags',             'TEXT DEFAULT ""'),
        ('rating',           'INTEGER DEFAULT 0'),
    ]
    
    for col_name, col_type in new_columns:
        try:
            cursor.execute(f"ALTER TABLE images ADD COLUMN {col_name} {col_type}")
        except sqlite3.OperationalError:
            pass   # colonna già esistente
            
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
        cursor.execute("SELECT id FROM images WHERE path=?", (path,))
        row = cursor.fetchone()
        return row[0] if row else None
    finally:
        conn.close()

def get_all_images():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM images ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def search_images(query: str):
    """Ricerca full-text su titolo, filename, tipo, costellazione, descrizione, tag, strumentazione, luogo."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    like = f"%{query}%"
    cursor.execute("""
        SELECT * FROM images
        WHERE title LIKE ? OR filename LIKE ? OR constellation LIKE ?
           OR description LIKE ? OR tags LIKE ? OR location LIKE ?
           OR type LIKE ? OR equipment LIKE ?
        ORDER BY id DESC
    """, (like, like, like, like, like, like, like, like))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def update_image(img_id, title, img_type, focal_length, focal_category, description,
                 ra, dec, constellation, equipment, integration_time, location,
                 date_acquired="", tags="", rating=0):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE images 
        SET title=?, type=?, focal_length=?, focal_category=?, description=?,
            ra=?, dec=?, constellation=?, equipment=?, integration_time=?, location=?,
            date_acquired=?, tags=?, rating=?
        WHERE id=?
    """, (title, img_type, focal_length, focal_category, description,
          ra, dec, constellation, equipment, integration_time, location,
          date_acquired, tags, rating, img_id))
    conn.commit()
    conn.close()

def delete_image(img_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM images WHERE id=?", (img_id,))
    conn.commit()
    conn.close()

def get_stats():
    """Restituisce statistiche aggregate del catalogo."""
    conn = get_connection()
    cursor = conn.cursor()
    stats = {}
    cursor.execute("SELECT COUNT(*) FROM images")
    stats['total'] = cursor.fetchone()[0]
    cursor.execute("SELECT type, COUNT(*) FROM images GROUP BY type ORDER BY COUNT(*) DESC")
    stats['by_type'] = cursor.fetchall()
    cursor.execute("SELECT COUNT(*) FROM images WHERE title != '' AND title IS NOT NULL")
    stats['titled'] = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM images WHERE ra != '' AND ra IS NOT NULL")
    stats['with_coords'] = cursor.fetchone()[0]
    conn.close()
    return stats

def export_to_csv(filepath: str):
    """Esporta tutte le immagini in un file CSV."""
    import csv
    images = get_all_images()
    if not images:
        return 0
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=images[0].keys())
        writer.writeheader()
        writer.writerows(images)
    return len(images)