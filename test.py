import flask 
import unittest
from Datahandler import app, init_db
import sqlite3

class TestMensajeriaSQLite(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()
        init_db()

    def setUp(self):
        init_db()

    def test_listar_contactos(self):
        response = self.app.get('/mensajeria/contactos?mialias=cpaz')
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.get_json(), {"Tipegod": "Tipe", "Alihew": "Napa"})

    def test_enviar_mensaje(self):
        response = self.app.post('/mensajeria/enviar', json={
            "usuario": "cpaz",
            "contacto": "lmunoz",
            "mensaje": "Hola Luisa"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("Mensaje enviado correctamente", response.get_data(as_text=True))

    def test_usuario_no_encontrado(self):
        response = self.app.get('/mensajeria/contactos?mialias=unknown')
        self.assertEqual(response.status_code, 404)
        self.assertIn("Usuario no encontrado", response.get_data(as_text=True))

    
    def test_contacto_invalido(self):
        response = self.app.post('/mensajeria/enviar', json={
            "usuario": "lmunoz",
            "contacto": "cpaz",
            "mensaje": "Hola Christian"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("El destinatario no es un contacto valido", response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()