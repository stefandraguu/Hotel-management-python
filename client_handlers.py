from flask import Flask, request, render_template, redirect, url_for
import sqlite3
from utils import get_db_connection
import random

def handle_client():
    """
    Preia și afișează informațiile despre camere, cazări și datele care se suprapun.
    """
    # Obținem conexiunea la baza de date
    conn = get_db_connection()
    cursor = conn.cursor()

    # Preluăm toate camerele
    cursor.execute('SELECT * FROM rooms')
    rooms = cursor.fetchall()

    # Preluăm toate cazările
    cursor.execute('SELECT * FROM accomodations')
    accomodations = cursor.fetchall()

    conn.close()

    # Calculăm suprapunerile de date pentru fiecare cameră
    overlapping_dates = {}
    for acc in accomodations:
        room_id = acc['room_id']
        if room_id not in overlapping_dates:
            overlapping_dates[room_id] = []
        overlapping_dates[room_id].append({
            'start': acc['date_start'].strftime('%Y-%m-%d'),
            'end': acc['date_end'].strftime('%Y-%m-%d')
        })

    # Renderizăm pagina clientului cu camerele și suprapunerile
    return render_template('client.html', rooms=rooms, accomodations=accomodations, overlapping_dates=overlapping_dates)

def handle_add_client_accomodation():
    """
    Adaugă o cazare pentru client, verificând dacă există suprapuneri în date.
    """
    # Generăm un ID unic pentru cazare
    id = random.randint(1, 2000)

    # Preluăm datele din formularul trimis de utilizator
    name = request.form.get('name')
    room_id = request.form.get('room_id')
    date_start = request.form.get('start-date')
    date_end = request.form.get('end-date')

    # Obținem conexiunea la baza de date
    conn = get_db_connection()
    cursor = conn.cursor()

    # Verificăm dacă ID-ul generat există deja
    cursor.execute('SELECT COUNT(*) FROM accomodations WHERE id = ?', (id,))
    if cursor.fetchone()[0] > 0:
        conn.close()
        return redirect(url_for('handle_actions', action="client-overview"))

    # Verificăm dacă există cazări pentru aceeași cameră
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

    # Verificăm dacă există suprapuneri cu alte cazări
    for accommodation in accommodations:
        if not (
            (date_start < accommodation["date_start"] and date_end < accommodation["date_start"]) or
            (date_start > accommodation["date_end"] and date_end > accommodation["date_end"])
        ):
            conn.close()
            return redirect(url_for('handle_actions', action="client"))

    # Inserăm cazarea nouă în baza de date
    cursor.execute('''
        INSERT INTO accomodations (id, room_id, date_start, date_end, name)
        VALUES (?, ?, ?, ?, ?)
    ''', (id, room_id, date_start, date_end, name))

    # Salvăm modificările și închidem conexiunea
    conn.commit()
    conn.close()

    return redirect(url_for('handle_actions', action="client"))
