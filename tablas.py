import sqlite3
import pytz
from datetime import datetime
from conexiones_db import fun_db_name

def fecha_hora_registro():
    hora_peru = pytz.timezone('America/Lima')
    hora_actual_peru = datetime.now(hora_peru)
    return hora_actual_peru.strftime('%Y-%m-%d')
# =============REGISTRO DE LOS VEHICULOS=============
def obtener_datos_entrada_salida_diccionario(sede):
    conn = sqlite3.connect(fun_db_name())
    cursor = conn.cursor()
    sql=''
    if(sede=='api'):
         sql = f'''
            SELECT r.id_vehiculo, v.sede, r.tipo, r.id_chofer ,p_chofer.nombre, p_chofer.telefono, p_chofer.rol,
            r.id_ayudante,p_ayudante.nombre, p_ayudante.telefono, p_ayudante.rol, r.sede, r.fecha_registro, r.observacion
            FROM registros_entrada_salida AS r
            INNER JOIN personal AS p_chofer ON p_chofer.id_personal=r.id_chofer
            INNER JOIN personal AS p_ayudante ON p_ayudante.id_personal=r.id_ayudante
            INNER JOIN vehiculo AS v ON v.id_vehiculo=r.id_vehiculo
            ORDER BY r.fecha_registro DESC
        '''       

    else:
        sql = f'''
            SELECT r.id_vehiculo, v.sede, r.tipo, r.id_chofer ,p_chofer.nombre, p_chofer.telefono, p_chofer.rol,
            r.id_ayudante,p_ayudante.nombre, p_ayudante.telefono, p_ayudante.rol, r.sede, r.fecha_registro, r.observacion
            FROM registros_entrada_salida AS r
            INNER JOIN personal AS p_chofer ON p_chofer.id_personal=r.id_chofer
            INNER JOIN personal AS p_ayudante ON p_ayudante.id_personal=r.id_ayudante
            INNER JOIN vehiculo AS v ON v.id_vehiculo=r.id_vehiculo
            WHERE substr(r.fecha_registro, 7, 4) || '-' || substr(r.fecha_registro, 4, 2) || '-' || substr(r.fecha_registro, 1, 2) = '{fecha_hora_registro()}'
            --AND r.sede={sede} --Estoy comentando esta línea para que todos vean los registros de todos.
            ORDER BY r.fecha_registro DESC
        '''
    cursor.execute(sql)
    data_tabla = cursor.fetchall()
    columnas_tabla = [description[0] for description in cursor.description]
    cursor.close()
    conn.close()

    # Construir una lista de diccionarios con los datos de la tabla
    lista_datos = []
    for fila in data_tabla:
        diccionario_fila = {
            'id_vehiculo': fila[0],
            'tipo_vehiculo': fila[1],
            'tipo_registro': fila[2],
            'id_chofer': fila[3],
            'nombre_chofer': fila[4],
            'telefono_chofer': fila[5],
            'rol_chofer': fila[6],
            'id_ayudante': fila[7],
            'nombre_ayudante': fila[8],
            'telefono_ayudante': fila[9],
            'rol_ayudante': fila[10],
            'sede': fila[11],
            'fecha_registro': fila[12],
            'observacion': fila[13]
        }
        lista_datos.append(diccionario_fila)

    return lista_datos

def arreglo_ua_de_datos_entrada_salida(sede): #Vehiculos
    ua=[]
    conn = sqlite3.connect(fun_db_name())
    cursor = conn.cursor()
    sql=f'''
        SELECT r.id_vehiculo, v.sede, r.tipo, r.id_chofer ,p_chofer.nombre, p_chofer.telefono, p_chofer.rol,
        r.id_ayudante,p_ayudante.nombre, p_ayudante.telefono, p_ayudante.rol, r.sede, r.fecha_registro, r.observacion
        FROM registros_entrada_salida AS r
        INNER JOIN personal AS p_chofer ON p_chofer.id_personal=r.id_chofer
        INNER JOIN personal AS p_ayudante ON p_ayudante.id_personal=r.id_ayudante
        INNER JOIN vehiculo AS v ON v.id_vehiculo=r.id_vehiculo
        WHERE substr(r.fecha_registro, 7, 4) || '-' || substr(r.fecha_registro, 4, 2) || '-' || substr(r.fecha_registro, 1, 2) = '{fecha_hora_registro()}'
        --AND r.sede={sede}        
        ORDER BY r.fecha_registro DESC
    '''
    cursor.execute(sql)
    registros_e_s = cursor.fetchall()
    cursor.close()
    conn.close()
    ua.append(registros_e_s)
    return ua
# =============REGISTRO DE LOS VEHICULOS=============


# =============REGISTRO DE LOS VISITANTES=============
def obtener_datos_entrada_salida_visitante_diccionario(sede):
    conn = sqlite3.connect(fun_db_name())
    cursor = conn.cursor()
    sql=''
    if(sede=='api'):
        sql=f'''
            SELECT rv.id_visitante,p_visitante.nombre,p_visitante.telefono,p_visitante.rol,
            rv.tipo,rv.area,rv.motivo_visita,rv.quien_autoriza,v_visitante.empresa,rv.fecha_registro
            FROM registros_visitante as rv
            INNER JOIN personal AS p_visitante ON p_visitante.id_personal=rv.id_visitante
            INNER JOIN visitante AS v_visitante ON v_visitante.id_visitante=rv.id_visitante    
            ORDER BY rv.fecha_registro DESC
        '''
    else:
        sql=f'''
            SELECT rv.id_visitante,p_visitante.nombre,p_visitante.telefono,p_visitante.rol,
            rv.tipo,rv.area,rv.motivo_visita,rv.quien_autoriza,v_visitante.empresa,rv.fecha_registro
            FROM registros_visitante as rv
            INNER JOIN personal AS p_visitante ON p_visitante.id_personal=rv.id_visitante
            INNER JOIN visitante AS v_visitante ON v_visitante.id_visitante=rv.id_visitante    
            WHERE substr(rv.fecha_registro, 7, 4) || '-' || substr(rv.fecha_registro, 4, 2) || '-' || substr(rv.fecha_registro, 1, 2) = '{fecha_hora_registro()}'
            ORDER BY rv.fecha_registro DESC
        '''
    cursor.execute(sql)
    data_tabla = cursor.fetchall()
    columnas_tabla = [description[0] for description in cursor.description]
    cursor.close()
    conn.close()

    # Construir una lista de diccionarios con los datos de la tabla
    lista_datos = []
    for fila in data_tabla:
        diccionario_fila = {
            'id_visitante': fila[0],
            'nombre': fila[1],
            'telefono': fila[2],
            'rol': fila[3],
            'tipo': fila[4],
            'area': fila[5],
            'motivo': fila[6],
            'autoriza': fila[7],
            'empresa': fila[8],
            'fecha_registro': fila[9]
        }
        lista_datos.append(diccionario_fila)

    return lista_datos

def arreglo_ua_de_datos_entrada_salida_visitante(): #Visitantes
    ua=[]
    conn = sqlite3.connect(fun_db_name())
    cursor = conn.cursor()
    sql=f'''
        SELECT rv.id_visitante,p_visitante.nombre,p_visitante.telefono,p_visitante.rol,
        rv.tipo,rv.area,rv.motivo_visita,rv.quien_autoriza,v_visitante.empresa,rv.fecha_registro,rv.observacion
        FROM registros_visitante as rv
        INNER JOIN personal AS p_visitante ON p_visitante.id_personal=rv.id_visitante
        INNER JOIN visitante AS v_visitante ON v_visitante.id_visitante=rv.id_visitante    
        WHERE substr(rv.fecha_registro, 7, 4) || '-' || substr(rv.fecha_registro, 4, 2) || '-' || substr(rv.fecha_registro, 1, 2) = '{fecha_hora_registro()}'
        ORDER BY rv.fecha_registro DESC
    '''
    cursor.execute(sql)
    registros_e_s = cursor.fetchall()
    cursor.close()
    conn.close()
    ua.append(registros_e_s)
    return ua
# =============REGISTRO DE LOS VISITANTES=============
