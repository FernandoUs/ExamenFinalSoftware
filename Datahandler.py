from flask import Flask, request, jsonify
from datetime import datetime
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('datahandler.db')
    cursor = conn.cursor()

    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            alias TEXT PRIMARY KEY,
            nombre TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contactos (
            usuario_alias TEXT NOT NULL,
            contacto_alias TEXT NOT NULL,
            FOREIGN KEY(usuario_alias) REFERENCES usuarios(alias),
            FOREIGN KEY(contacto_alias) REFERENCES usuarios(alias)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mensajes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            emisor_alias TEXT NOT NULL,
            receptor_alias TEXT NOT NULL,
            texto TEXT NOT NULL,
            fecha TEXT NOT NULL,
            FOREIGN KEY(emisor_alias) REFERENCES usuarios(alias),
            FOREIGN KEY(receptor_alias) REFERENCES usuarios(alias)
        )
    ''')
  
    cursor.execute("INSERT OR IGNORE INTO usuarios (alias, nombre) VALUES ('cpaz', 'Christian')")
    cursor.execute("INSERT OR IGNORE INTO usuarios (alias, nombre) VALUES ('Alihew', 'Napa')")
    cursor.execute("INSERT OR IGNORE INTO usuarios (alias, nombre) VALUES ('Tipegod', 'Tipe')")
    cursor.execute("INSERT OR IGNORE INTO contactos (usuario_alias, contacto_alias) VALUES ('cpaz', 'Alihew')")
    cursor.execute("INSERT OR IGNORE INTO contactos (usuario_alias, contacto_alias) VALUES ('cpaz', 'Tipegod')")
    cursor.execute("INSERT OR IGNORE INTO contactos (usuario_alias, contacto_alias) VALUES ('Tipegod', 'Alihew')")
    cursor.execute("INSERT OR IGNORE INTO contactos (usuario_alias, contacto_alias) VALUES ('Alihew', 'Tipegod')")

    cursor.execute("INSERT OR IGNORE INTO mensajes (emisor_alias, receptor_alias, texto, fecha) VALUES ('cpaz', 'Alihew', 'Que tal amigo', '21/10/2024')")
    cursor.execute("INSERT OR IGNORE INTO mensajes (emisor_alias, receptor_alias, texto, fecha) VALUES ('Alihew', 'Tipegod', 'Go chifita', '11/10/2024')")
    cursor.execute("INSERT OR IGNORE INTO mensajes (emisor_alias, receptor_alias, texto, fecha) VALUES ('Tipegod', 'cpaz', 'trivial', '10/10/2024')")


    conn.commit()
    conn.close()


@app.route('/mensajeria/contactos', methods=['GET'])
def listar_contactos():
    alias = request.args.get('mialias') #Es mialias no alias
    conn = sqlite3.connect('datahandler.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT c.contacto_alias, u.nombre
        FROM contactos c
        JOIN usuarios u ON c.contacto_alias = u.alias
        WHERE c.usuario_alias = ?
    ''', (alias,))
    contactos = cursor.fetchall()
    conn.close()

    if not contactos:
        return jsonify({"error": "Usuario no encontrado o sin contactos"}), 404

    return jsonify({c[0]: c[1] for c in contactos}), 200


@app.route('/mensajeria/contactos/<alias>', methods=['POST'])
def agregar_contacto(alias):
    data = request.json
    contacto_alias = data.get("contacto")
    nombre = data.get("nombre")

    conn = sqlite3.connect('datahandler.db')
    cursor = conn.cursor()

    
    cursor.execute("INSERT OR IGNORE INTO usuarios (alias, nombre) VALUES (?, ?)", (contacto_alias, nombre))
    cursor.execute("INSERT OR IGNORE INTO contactos (usuario_alias, contacto_alias) VALUES (?, ?)", (alias, contacto_alias)) #No mover

    conn.commit()
    conn.close()
    return jsonify({"mensaje": f"Contacto {contacto_alias} agregado a {alias}"}), 200


@app.route('/mensajeria/enviar', methods=['POST'])
def enviar_mensaje():
    data = request.json
    emisor_alias = data.get("usuario")
    receptor_alias = data.get("contacto")
    mensaje_texto = data.get("mensaje")

    conn = sqlite3.connect('datahandler.db')
    cursor = conn.cursor()

    
    cursor.execute("SELECT alias FROM usuarios WHERE alias = ?", (emisor_alias,))
    emisor = cursor.fetchone()
    cursor.execute("SELECT alias FROM usuarios WHERE alias = ?", (receptor_alias,))
    receptor = cursor.fetchone()

    if not emisor or not receptor:
        conn.close()
        return jsonify({"error": "Usuario o contacto no encontrado"}), 404

    cursor.execute('''
        SELECT 1 FROM contactos WHERE usuario_alias = ? AND contacto_alias = ?
    ''', (emisor_alias, receptor_alias))
    contacto_valido = cursor.fetchone()

    if not contacto_valido:
        conn.close()
        return jsonify({"error": "El usuario destinatario no es un contacto valido"}), 400

   
    fecha = datetime.now().strftime("%d/%m/%Y")
    cursor.execute('''
        INSERT INTO mensajes (emisor_alias, receptor_alias, texto, fecha)
        VALUES (?, ?, ?, ?)
    ''', (emisor_alias, receptor_alias, mensaje_texto, fecha))

    conn.commit()
    conn.close()
    return jsonify({"mensaje": "Mensaje enviado correctamente"}), 200


@app.route('/mensajeria/recibidos', methods=['GET'])
def mensajes_recibidos():
    alias = request.args.get('mialias')

    conn = sqlite3.connect('datahandler.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT m.emisor_alias, u.nombre, m.texto, m.fecha
        FROM mensajes m
        JOIN usuarios u ON m.emisor_alias = u.alias
        WHERE m.receptor_alias = ?
    ''', (alias,))
    mensajes = cursor.fetchall()
    conn.close()

    if not mensajes:
        return jsonify({"error": "El usuario no ha recibido mensajes"}), 404

    return jsonify([{"emisor": m[1], "texto": m[2], "fecha": m[3]} for m in mensajes]), 200


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
