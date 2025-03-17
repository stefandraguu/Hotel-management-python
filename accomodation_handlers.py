from flask import Flask, request, render_template, redirect, url_for
import sqlite3
from utils import get_db_connection
from datetime import datetime
import random

def handle_add_accomodation():
    # Preluăm datele din formularul trimis de utilizator
    name = request.form.get('name')
    room_id = request.form.get('room_id')
    date_start = request.form.get('start-date')
    date_end = request.form.get('end-date')

    # Obținem conexiunea la baza de date
    conn = get_db_connection()
    cursor = conn.cursor()

    # Generăm un ID unic pentru cazare
    id = random.randint(1, 2000)

    # Verificăm dacă există alte cazări pentru aceeași cameră
    cursor.execute('SELECT * FROM accomodations WHERE room_id = ?', (room_id,))
    rows = cursor.fetchall()

    # Transformăm rezultatele interogării într-o listă de dicționare pentru procesare ușoară
    accommodations = [
        {
            "id": row["id"],
            "room_id": row["room_id"],
            "date_start": row["date_start"],
            "date_end": row["date_end"],
            "name": row["name"]
        }
        for row in rows
    ]

    # Verificăm suprapunerile cu alte perioade de cazare
    for accommodation in accommodations:
        if not (
            (date_start < accommodation["date_start"] and date_end < accommodation["date_start"]) or
            (date_start > accommodation["date_end"] and date_end > accommodation["date_end"])
        ):
            conn.close()
            return redirect(url_for('handle_actions', action="manage_accomodations"))

    # Verificăm dacă ID-ul generat există deja
    cursor.execute('SELECT COUNT(*) FROM accomodations WHERE id = ?', (id,))
    if cursor.fetchone()[0] > 0:
        conn.close()
        return redirect(url_for('handle_actions', action="manage_accomodations"))

    # Inserăm noua cazare în baza de date
    cursor.execute('''
        INSERT INTO accomodations (id, room_id, date_start, date_end, name)
        VALUES (?, ?, ?, ?, ?)
    ''', (id, room_id, date_start, date_end, name))

    # Salvăm modificările și închidem conexiunea
    conn.commit()
    conn.close()
    return redirect(url_for('handle_actions', action="manage_accomodations"))

def handle_delete_accomodation():
    # Preluăm ID-ul și rating-ul din formularul trimis
    id = request.form.get('id')
    rating = request.form.get('rating')

    # Obținem conexiunea la baza de date
    conn = get_db_connection()
    cursor = conn.cursor()

    # Selectăm camera asociată cazării ce urmează a fi ștearsă
    cursor.execute('SELECT room_id FROM accomodations WHERE id = ?', (id,))
    room_id_result = cursor.fetchone()

    # Ștergem cazarea din baza de date
    cursor.execute('DELETE FROM accomodations WHERE id = ? ', (id,))
    conn.commit()

    # Actualizăm rating-ul camerei
    cursor.execute('''
        UPDATE rooms
        SET no_ratings = no_ratings + 1,
            rating = rating + ?
        WHERE id = ?
    ''', (rating, room_id_result[0]))
    conn.commit()

    # Închidem conexiunea la baza de date
    conn.close()

    return redirect(url_for('handle_actions', action="manage_accomodations"))
