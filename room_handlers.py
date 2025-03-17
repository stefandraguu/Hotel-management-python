from flask import Flask, request, render_template, redirect, url_for
import sqlite3
from utils import get_db_connection
from datetime import date, timedelta, datetime

# Funcția care adaugă o cameră nouă în baza de date
def handle_add_room():
    room_id = request.form.get('id')
    beds = request.form.get('beds')
    ppn = request.form.get('ppn')
    rating = 0  # Rating-ul implicit este 0
    no_ratings = 0  # Numărul implicit de evaluări este 0

    # Conectăm la baza de date
    conn = get_db_connection()
    cursor = conn.cursor()

    # Verificăm dacă ID-ul camerei există deja
    cursor.execute('SELECT COUNT(*) FROM rooms WHERE id = ?', (room_id,))
    if cursor.fetchone()[0] > 0:
        conn.close()
        return redirect(url_for('handle_actions', action="manage_rooms"))

    # Inserăm camera nouă în tabelul 'rooms'
    cursor.execute('''
        INSERT INTO rooms (id, beds, ppn, rating, no_ratings)
        VALUES (?, ?, ?, ?, ?)
    ''', (int(room_id), int(beds), int(ppn), rating, no_ratings))
    conn.commit()
    conn.close()
    return redirect(url_for('handle_actions', action="manage_rooms"))

# Funcția care șterge o cameră din baza de date
def handle_delete_room():
    room_id = request.form.get('id')

    # Validăm input-ul
    conn = get_db_connection()
    cursor = conn.cursor()

    # Ștergem camera cu ID-ul specificat
    cursor.execute('DELETE FROM rooms WHERE id = ? ', (room_id,))
    conn.commit()

    # Închidem conexiunea la baza de date
    conn.close()
    
    return redirect(url_for('handle_actions', action="manage_rooms"))
