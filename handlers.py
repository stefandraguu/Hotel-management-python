from flask import Flask, request, render_template, redirect, url_for
import sqlite3
from utils import get_db_connection
from datetime import date, timedelta, datetime

# Funcția care returnează pagina principală
def home():
    return render_template('index.html')

# Funcția care gestionează redirecționările în funcție de acțiunea solicitată
def handle_redirects():
    # Preluăm valoarea 'action' din formularul trimis
    action = request.form.get('action')
    # Redirecționăm către ruta 'handle_actions' cu 'action' ca parametru URL
    return redirect(url_for("handle_actions", action=action))

# Funcția care gestionează acțiunile pe baza parametrului 'action'
def handle_actions(action):
    # Conectăm la baza de date
    conn = get_db_connection()
    cursor = conn.cursor()

    # Preluăm toate camerele
    cursor.execute('SELECT * FROM rooms')  
    rooms = cursor.fetchall()

    # Preluăm toate cazărilor
    cursor.execute('SELECT * FROM accomodations')
    rows = cursor.fetchall()

    conn.close()

    # Creăm un dicționar pentru calendarele camerelor
    calendars = {}
    accomodations = [dict(row) for row in rows]

    # Convertim datele din șiruri de caractere în obiecte de tip 'date'
    for accomodation in accomodations:
        accomodation['date_start'] = (
            datetime.strptime(accomodation['date_start'], "%Y-%m-%d").date()
            if accomodation['date_start'] is not None
            else date(2024, 12, 1)
        )
        accomodation['date_end'] = (
            datetime.strptime(accomodation['date_end'], "%Y-%m-%d").date()
            if accomodation['date_end'] is not None
            else date(2024, 12, 31)
        )

    # Generăm calendarele pentru fiecare cameră
    for room in rooms:
        room_id = room['id']
        start_date = date(2024, 12, 1)  # Data de început a lunii
        end_date = date(2024, 12, 31)  # Data de sfârșit a lunii
        calendar = []
        current_date = start_date
        
        # Verificăm pentru fiecare zi din interval dacă camera este rezervată
        while current_date <= end_date:
            is_booked = any(
                current_date >= accomodation['date_start'] and
                current_date <= accomodation['date_end'] and
                accomodation['room_id'] == room_id
                for accomodation in accomodations
            )

            calendar.append({'date': current_date, 'is_booked': is_booked})
            current_date += timedelta(days=1)
        
        calendars[room_id] = calendar

    # Renderizăm pagina specifică acțiunii cu informațiile despre camere și cazări
    return render_template(f'{action}.html', rooms=rooms, accomodations=accomodations, calendars=calendars)
