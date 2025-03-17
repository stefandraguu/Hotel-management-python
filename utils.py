from flask import Flask, request, render_template, redirect, url_for
import sqlite3

# Funcția care se conectează la baza de date SQLite și returnează conexiunea
def get_db_connection():
    # Creăm o conexiune la baza de date 'mydatabase.db'
    conn = sqlite3.connect('mydatabase.db')

    # Setăm fabrica de rânduri (row_factory) astfel încât să putem accesa fiecare coloană ca pe un dicționar
    conn.row_factory = sqlite3.Row  

    # Returnăm obiectul de conexiune
    return conn
