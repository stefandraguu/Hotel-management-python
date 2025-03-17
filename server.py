from flask import Flask, request, render_template, redirect, url_for
from room_handlers import handle_add_room, handle_delete_room
from accomodation_handlers import handle_add_accomodation, handle_delete_accomodation
from client_handlers import handle_client, handle_add_client_accomodation
from handlers import home, handle_redirects, handle_actions

# Crearea unei aplicații Flask
app = Flask(__name__)

# Definirea route-urilor pentru fiecare funcționalitate

# Ruta principală (pagina de start) - Servește formularul HTML
app.add_url_rule('/', 'home', home, methods=['GET', 'POST'])

# Ruta care gestionează redirecționările pe baza acțiunii primite din formular
app.add_url_rule('/action_handler', 'handle_redirects', handle_redirects, methods=['POST'])

# Ruta care gestionează acțiunile (ex: vizualizare sau modificare de camere/cazări) pe baza acțiunii transmise
app.add_url_rule('/actions/<string:action>', 'handle_actions', handle_actions, methods=['GET'])

# Ruta pentru adăugarea unei camere noi
app.add_url_rule('/add_room', 'handle_add_room', handle_add_room, methods=['POST'])

# Ruta pentru ștergerea unei camere
app.add_url_rule('/delete_room', 'handle_delete_room', handle_delete_room, methods=['POST'])

# Ruta pentru adăugarea unei noi cazări
app.add_url_rule('/add_accomodation', 'handle_add_accomodation', handle_add_accomodation, methods=['POST'])

# Ruta pentru ștergerea unei cazări
app.add_url_rule('/delete_accomodation', 'handle_delete_accomodation', handle_delete_accomodation, methods=['POST'])

# Ruta pentru vizualizarea informațiilor clientului
app.add_url_rule('/client', 'handle_client', handle_client, methods=['GET'])

# Ruta pentru adăugarea unei cazări pentru un client
app.add_url_rule('/add_client_accomodation', 'handle_add_client_accomodation', handle_add_client_accomodation, methods=['POST'])

# Pornirea aplicației în modul de depanare (debug)
if __name__ == '__main__':
    app.run(debug=True)
