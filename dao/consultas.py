from dao.conexiondb import ConexionDB
from datetime import datetime

def crear_tabla():
    try:
        condb = ConexionDB()

        sql_reclamosTipos = '''
            CREATE TABLE IF NOT EXISTS reclamosTipos(
            idReclamoTipo INTEGER NOT NULL,
            descripcion VARCHAR(256) NOT NULL,
            PRIMARY KEY(idReclamoTipo AUTOINCREMENT)
            );
        '''
        
        sql_reclamosEstados = '''
            CREATE TABLE IF NOT EXISTS reclamosEstados(
            idReclamoEstado INTEGER NOT NULL,
            descripcion VARCHAR(256) NOT NULL,
            PRIMARY KEY(idReclamoEstado AUTOINCREMENT)
            );
        '''
        
        sql_reclamos = '''
            CREATE TABLE IF NOT EXISTS reclamos(
            idReclamo INTEGER NOT NULL,
            asunto VARCHAR(256) NOT NULL,
            descripcion VARCHAR(256),
            fechaCreado DATETIME NOT NULL,
            idReclamoEstado INTEGER NOT NULL,
            idReclamoTipo INTEGER NOT NULL,
            PRIMARY KEY(idReclamo AUTOINCREMENT),
            FOREIGN KEY(idReclamoTipo) REFERENCES reclamosTipos(idReclamoTipo),
            FOREIGN KEY(idReclamoEstado) REFERENCES reclamosEstados(idReclamoEstado)
            );
        '''
        
        condb.cursor.execute(sql_reclamosTipos)
        condb.cursor.execute(sql_reclamosEstados)
        condb.cursor.execute(sql_reclamos)
        condb.cerrar_conexion()
    except Exception as e:
        print(e)


def agregar_datos():
    try:
        condb = ConexionDB()

        sql1 = '''
                INSERT INTO reclamosTipos(descripcion) VALUES ('Falla de motor'), ('Falla electrica'), ('Falla de suspensión'), ('Falla de frenos'), ('Servicio Post-Venta'), ('Aprobación de cobertura'), ('Reemplazo de piezas'), ('Reembolso')
        '''
        sql2 = '''
                INSERT INTO reclamosEstados(descripcion) VALUES ('Creado'), ('Modificado'), ('Finalizado')
        '''

        condb.cursor.execute(sql1)
        condb.cursor.execute(sql2)
        condb.cerrar_conexion()
    except Exception as e:
        print(e)

def listar_reclamos():
    try:
        condb = ConexionDB()
        listar_reclamos = []

        sql= f'''
            SELECT r.idReclamo, r.asunto, r.descripcion, rt.descripcion, re.descripcion, fechaCreado FROM reclamos as r
            INNER JOIN reclamosTipos as rt ON r.idReclamoTipo = rt.idReclamoTipo
            INNER JOIN reclamosEstados as re ON r.idReclamoEstado = re.idReclamoEstado;
        '''
        condb.cursor.execute(sql)
        listar_reclamos = condb.cursor.fetchall()
        condb.cerrar_conexion()

        return listar_reclamos
    except Exception as e:
        print(e)

def crear_reclamo(asunto, descripcion, reclamoTipo):
    try:
        condb = ConexionDB()
        now = datetime.now().strftime(f"%d/%m/%Y %H:%M:%S")
        id_reclamo_tipo = obtener_tipo(reclamoTipo)

        sql= f'''
            INSERT INTO reclamos(asunto, descripcion, idReclamoTipo, idReclamoEstado, fechaCreado)
            VALUES('{asunto}','{descripcion}', {id_reclamo_tipo}, {1}, '{now}');
        '''
        condb.cursor.execute(sql)
        condb.cerrar_conexion()
    except Exception as e:
        print(e)


def modificar_reclamo(id, asunto, descripcion, reclamoTipo):
    try:
        condb = ConexionDB()
        id_reclamo_tipo = obtener_tipo(reclamoTipo)

        sql= f'''
            UPDATE reclamos SET asunto = '{asunto}', descripcion = '{descripcion}', idReclamoTipo = {id_reclamo_tipo}, idReclamoEstado = {2}
            WHERE idReclamo = {id};
        '''

        condb.cursor.execute(sql)
        condb.cerrar_conexion()
    except Exception as e:
        print(e)

def borrar_reclamo(id):
    try:
        condb = ConexionDB()

        sql= f'''
            DELETE FROM reclamos
            WHERE idReclamo = {id};
        '''

        condb.cursor.execute(sql)
        condb.cerrar_conexion()
    except Exception as e:
        print(e)

def listar_tipos():
    try:
        condb = ConexionDB()

        sql = f'''
            SELECT * FROM reclamosTipos;
        '''
        condb.cursor.execute(sql)
        listar_reclamo_tipos = condb.cursor.fetchall()
        condb.cerrar_conexion()

        return listar_reclamo_tipos
    except Exception as e:
        print(e)

def obtener_tipo(reclamoTipo):
    try:
        condb = ConexionDB()

        sql = f'''
            SELECT idReclamoTipo FROM reclamosTipos
            WHERE descripcion = '{reclamoTipo}';
        '''

        condb.cursor.execute(sql)
        tipo = condb.cursor.fetchone()
        condb.cerrar_conexion()

        return tipo[0]
    except Exception as e:
        print(e)

def crear_tipo(descripcion):
    try:
        condb = ConexionDB()

        sql= f'''
            INSERT INTO reclamosTipos(descripcion)
            VALUES('{descripcion}');
        '''
        condb.cursor.execute(sql)
        condb.cerrar_conexion()
    except Exception as e:
        print(e)


def modificar_tipo(id, descripcion):
    try:
        condb = ConexionDB()

        sql= f'''
            UPDATE reclamosTipos SET descripcion = '{descripcion}'
            WHERE idReclamoTipo = {id};
        '''

        condb.cursor.execute(sql)
        condb.cerrar_conexion()
    except Exception as e:
        print(e)

def borrar_tipo(id):
    try:
        condb = ConexionDB()

        sql= f'''
            DELETE FROM reclamosTipos
            WHERE idReclamoTipo = {id};
        '''

        condb.cursor.execute(sql)
        condb.cerrar_conexion()
    except Exception as e:
        print(e)