import sqlite3

# Conectare la baza de date SQLite (se va crea fișierul dacă nu există)
conn = sqlite3.connect('mydatabase.db')  # 'mydatabase.db' este fișierul bazei de date SQLite
cursor = conn.cursor()

# Crearea unui tabel nou numit 'rooms' pentru stocarea informațiilor despre camere
cursor.execute('''
CREATE TABLE IF NOT EXISTS rooms (
    id INTEGER,         -- Identificatorul unic al camerei
    beds INTEGER,       -- Numărul de paturi din cameră
    ppn INTEGER,        -- Preț pe noapte (PPN - price per night)
    rating REAL,        -- Rating-ul camerei
    no_ratings INTEGER  -- Numărul de evaluări ale camerei
)
''')

# Crearea unui tabel nou numit 'accomodations' pentru stocarea informațiilor despre cazări
cursor.execute('''
CREATE TABLE IF NOT EXISTS accomodations (
    id INTEGER,         -- Identificatorul unic al cazarii
    room_id INTEGER,    -- ID-ul camerei asociate cu cazarea
    date_start DATE,    -- Data de început a cazării
    date_end DATE,      -- Data de sfârșit a cazării
    name TEXT           -- Numele clientului asociat cazarii
)
''')

# Comitere a modificărilor în baza de date
conn.commit()

# Închidem conexiunea la baza de date
conn.close()
