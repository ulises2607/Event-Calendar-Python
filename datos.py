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
    """Insertar datos para la primera manipulación"""

    datos_fechas = [
        (1,'2023-07-20',),
        (2,'2023-07-21',),
        (3, '2023-07-26')
    ]

    datos_eventos = [
        (1, 1, "Evento 1", "09:00:00", 60, "Descripción 1", "normal"),
        (1, 2, "Evento 2", "14:30:00", 90, "Descripción 2", "importante"),
        (1, 3, "Evento 3", "16:00:00", 45, "Descripción 3", "normal"),
        (2, 4, "Evento 4", "10:15:00", 120, "Descripción 4", "importante"),
        (2, 5, "Evento 5", "11:30:00", 30, "Descripción 5", "normal"),
        (3, 1, "Evento 6", "09:00:00", 60, "Descripción 6", "normal"),
        (3, 2, "Evento 7", "14:30:00", 90, "Descripción 7", "importante"),
        (3, 3, "Evento 8", "16:00:00", 45, "Descripción 8", "normal"),
        (2, 4, "Evento 9", "10:15:00", 120, "Descripción 9", "importante"),
        (2, 5, "Evento 10", "11:30:00", 30, "Descripción 10", "normal")
    ]
    datos_etiquetas = [
        ("Otros",),
        ("Universidad",),
        ("Trabajo",),
        ("Otros",),
        ("Pasatiempo",),
        ("Trabajo",),
        ("Otros",),
        ("Universidad",),
        ("Trabajo",),
        ("Otros",),
        ("Pasatiempo",),
        ("Trabajo",)
    ]


    query_eventos = "INSERT INTO Eventos (id_fecha, id_etiqueta, titulo_evento, hora_evento, duracion_minutos, descripcion, importancia) \
        VALUES (%s, %s, %s, %s, %s, %s, %s)"
    query_etiquetas = "INSERT INTO Etiquetas (etiqueta) VALUES (%s)"

    query_fechas = "INSERT INTO Fechas (id_fecha, fecha) VALUES (%s, %s)"

    conn = conectar()
    cur = conn.cursor()
    cur.executemany(query_fechas, datos_fechas)
    cur.executemany(query_etiquetas, datos_etiquetas)
    cur.executemany(query_eventos, datos_eventos)
    conn.commit()
    conn.close()

def filtrarDatos(fech, etiquet):
    query = "SELECT id_evento, titulo_evento, hora_evento, duracion_minutos, descripcion, importancia, Etiquetas.etiqueta \
            FROM Eventos\
            JOIN Etiquetas ON Eventos.id_etiqueta = Etiquetas.id_etiqueta\
            JOIN Fechas ON Eventos.id_fecha = Fechas.id_fecha\
            WHERE Fechas.fecha = %s AND Etiquetas.etiqueta = %s;"

    datos = (fech, etiquet)

    conn = conectar()
    cur = conn.cursor()
    cur.execute(query, datos)
    result = cur.fetchall()  # Recupera los datos del resultado

    # Cierra el cursor y la conexión
    cur.close()
    conn.close()

    return result


def eliminarEvento(id_evento):
    query = "DELETE FROM Eventos WHERE id_evento = %s"

    conn = conectar()
    cur = conn.cursor()
    cur.execute(query, (id_evento,))
    conn.commit()
    conn.close()

def agregarDatos(fecha_param,etiqueta,event):
    
    query_fechas = "INSERT INTO Fechas (fecha) VALUES (%s)"
    query_etiquetas = "INSERT INTO Etiquetas (etiqueta) VALUES (%s)"
    query_eventos = "INSERT INTO Eventos (id_fecha, id_etiqueta, titulo_evento, hora_evento, duracion_minutos, descripcion, importancia) \
    VALUES (%s,%s,%s, %s, %s, %s, %s)"

    

    conn = conectar()
    cur = conn.cursor()
    cur.execute(query_fechas, fecha_param)
    id_fecha_generado = cur.lastrowid
    cur.execute(query_etiquetas, etiqueta)
    id_etiqueta_generado = cur.lastrowid

    datosEvento = (id_fecha_generado, id_etiqueta_generado, event[0], event[1], event[2], event[3], event[4])
    cur.execute(query_eventos, datosEvento)
    conn.commit()
    conn.close()


def buscarFecha(date):
    query ="SELECT id_fecha FROM Fechas WHERE Fechas.fecha = %s"
    conn= conectar()
    cur = conn.cursor()
    cur.execute(query, (date,))
    datos = cur.fetchall()
    conn.close()
    
    return datos

def obtenerDatosGral(date): 
    query ="SELECT id_evento, titulo_evento, hora_evento, duracion_minutos, descripcion, importancia, Etiquetas.etiqueta FROM Eventos\
            JOIN Etiquetas ON Eventos.id_etiqueta = Etiquetas.id_etiqueta\
            JOIN Fechas ON Eventos.id_fecha = Fechas.id_fecha\
            WHERE Fechas.fecha = %s;"
    conn= conectar()
    cur = conn.cursor()
    cur.execute(query, (date,))
    datos = cur.fetchall()
    cur.close()
    conn.close()
    
    return datos

def obtenerDatosEtiquetas():
    query = 'SELECT etiqueta FROM Etiquetas'
    conn = conectar()
    cur = conn.cursor()
    cur.execute(query)
    datos = cur.fetchall()
    conn.close()

    return datos
    
def create_if_not_exist():
    """Crea la base de datos y la tabla si no existen.
    
    Esto asegura que la aplicacion funcione aunque no
    exista la base de datos previamente.
    Si es necesario que exista el usuario (con sus respectivos permisos)
    en el servidor.
    """
    create_database = "CREATE DATABASE IF NOT EXISTS %s" %config.credenciales["database"]
    create_table_fecha = '''
                            CREATE TABLE IF NOT EXISTS Fechas (
                                id_fecha INT UNIQUE PRIMARY KEY AUTO_INCREMENT,
                                fecha DATE
                            );
    '''
    create_table_etiquetas = '''CREATE TABLE IF NOT EXISTS Etiquetas (
                                    id_etiqueta INT PRIMARY KEY AUTO_INCREMENT,
                                    etiqueta varchar(60)
                                );
    '''
    create_table_eventos = '''CREATE TABLE IF NOT EXISTS Eventos (
                        id_evento int NOT NULL UNIQUE AUTO_INCREMENT,
                        id_fecha int,
                        id_etiqueta int,
                        titulo_evento varchar(60) NOT NULL,
                        hora_evento TIME,
                        duracion_minutos INTEGER,
                        descripcion varchar(100),
                        importancia varchar(20) default 'normal',
                        FOREIGN KEY (id_fecha) REFERENCES Fechas(id_fecha),
                        FOREIGN KEY (id_etiqueta) REFERENCES Etiquetas(id_etiqueta)
                        );
    '''
    
    
    
    try:
        conn = mysql.connector.connect(user=config.credenciales["user"],
                                       password=config.credenciales["password"],
                                       host="127.0.0.1")
        cur = conn.cursor()
        cur.execute(create_database)
        cur.execute("USE %s" %config.credenciales["database"])
        cur.execute(create_table_fecha)
        cur.execute(create_table_etiquetas)
        cur.execute(create_table_eventos)
        conn.commit()
        conn.close()

        # insertarDatos()

    except errors.DatabaseError as err:
        print("Error al conectar o crear la base de datos.", err)
        raise