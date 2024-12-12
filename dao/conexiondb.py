import sqlite3

class ConexionDB():
    def __init__(self):
        self.base_de_datos = 'database/Reclamos.db'
        self.conexion = sqlite3.connect(self.base_de_datos)
        self.cursor = self.conexion.cursor()

    def cerrar_conexion(self):
        self.conexion.commit()
        self.conexion.close()

