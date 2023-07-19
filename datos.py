import mysql.connector
from mysql.connector import errors
import config

def conectar():
    """Conectar con la base de datos y devolver un obj conexion."""
    try:
        conn = mysql.connector.connect(**config.credenciales)
    except errors.DatabaseError as err:
        print("Error al conectar.", err)
    else:
        return conn

def insertarDatos():
    """ Insertar datos para primera manipulacion"""
    datos_eventos = [
        ("Evento 1", "2023-07-18 09:00:00", 60, "Descripción 1", "normal"),
        ("Evento 2", "2023-07-19 14:30:00", 90, "Descripción 2", "importante"),
        ("Evento 3", "2023-07-20 16:00:00", 45, "Descripción 3", "normal"),
        ("Evento 4", "2023-07-21 10:15:00", 120, "Descripción 4", "importante"),
        ("Evento 5", "2023-07-22 11:30:00", 30, "Descripción 5", "normal")
    ]
    query = "INSERT INTO Eventos (titulo_evento, fecha_hora, duracion_minutos, descripcion, importancia) \
        VALUES (%s, %s, %s, %s, %s)"
    
    conn = conectar()
    cur = conn.cursor()
    cur.executemany(query, datos_eventos)
    conn.commit()
    conn.close()



    
def create_if_not_exist():
    """Crea la base de datos y la tabla si no existen.
    
    Esto asegura que la aplicacion funcione aunque no
    exista la base de datos previamente.
    Si es necesario que exista el usuario (con sus respectivos permisos)
    en el servidor.
    """
    create_database = "CREATE DATABASE IF NOT EXISTS %s" %config.credenciales["database"]
    create_table_eventos = """CREATE TABLE IF NOT EXISTS Eventos (
                        id_evento int  NOT NULL UNIQUE AUTO_INCREMENT,
                        titulo_evento varchar(60) NOT NULL,
                        fecha_hora DATETIME,
                        duracion_minutos INTEGER,
                        descripcion varchar(100),
                        importancia varchar(20) default 'normal'
                        )"""
    create_table_etiquetas = '''CREATE TABLE IF NOT EXISTS Etiquetas (
                                    id_etiqueta INTEGER UNIQUE PRIMARY KEY AUTO_INCREMENT,
                                    etiqueta varchar(60)
                                )
    '''
    create_table_ev_etiq = '''
                            CREATE TABLE IF NOT EXISTS Eventos_Etiquetas (
                                id_evento INT,
                                id_etiqueta INT,
                                FOREIGN KEY (id_evento) REFERENCES Eventos(id_evento),
                                FOREIGN KEY (id_etiqueta) REFERENCES Etiquetas(id_etiqueta),
                                PRIMARY KEY (id_evento, id_etiqueta)
                            )
    '''
    
    try:
        conn = mysql.connector.connect(user=config.credenciales["user"],
                                       password=config.credenciales["password"],
                                       host="127.0.0.1")
        cur = conn.cursor()
        cur.execute(create_database)
        cur.execute("USE %s" %config.credenciales["database"])
        cur.execute(create_table_eventos)
        cur.execute(create_table_etiquetas)
        cur.execute(create_table_ev_etiq)
        conn.commit()
        conn.close()
    except errors.DatabaseError as err:
        print("Error al conectar o crear la base de datos.", err)
        raise