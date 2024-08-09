import sqlite3
import time
bd_name ='seguridad.db'

def fun_db_name():
    return bd_name

def validar_usuario(id_user):
    conn = sqlite3.connect(bd_name)
    cursor = conn.cursor()
    cursor.execute("SELECT id_user, user, pass, rol, sede FROM credenciales WHERE id_user = ?", (id_user,))
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    return resultado

def registrar_e_s_vehiculos(vehiculo,conductor,ayudante,tipo_e_s,sede,fh_r,observacion):
    conn = sqlite3.connect(bd_name)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO registros_entrada_salida (id_vehiculo, id_chofer, id_ayudante, tipo, sede, fecha_registro, observacion) VALUES (?,?,?,?,?,?,?)",
                   (vehiculo, conductor, ayudante, tipo_e_s, sede, fh_r, observacion))
    conn.commit()
    cursor.close()
    conn.close()

def obtener_detalles_persona(id_persona):
    conn = sqlite3.connect(bd_name)
    cursor = conn.cursor()
    cursor = conn.cursor()
    cursor.execute("SELECT id_personal, nombre, telefono FROM personal WHERE id_personal = ?", (id_persona,))
    resultado=cursor.fetchone()
    cursor.close()
    conn.close()
    return resultado

def obtener_imagen_persona(id_persona):
    conn = sqlite3.connect(bd_name)
    cursor = conn.cursor()
    cursor = conn.cursor()
    cursor.execute("SELECT foto_personal FROM personal WHERE id_personal = ?", (id_persona,))
    resultado=cursor.fetchone()
    cursor.close()
    conn.close()
    return resultado

def obtener_detalle_vehiculo(id_vehiculo):
    conn = sqlite3.connect(bd_name)
    cursor = conn.cursor()
    cursor = conn.cursor()
    cursor.execute("SELECT id_vehiculo,sede FROM vehiculo WHERE id_vehiculo = ?", (id_vehiculo,))
    resultado=cursor.fetchone()
    cursor.close()
    conn.close()
    return resultado

def obtener_imagen_vehiculo(id_vehiculo):
    conn = sqlite3.connect(bd_name)
    cursor = conn.cursor()
    cursor = conn.cursor()
    cursor.execute("SELECT foto_vehiculo FROM vehiculo WHERE id_vehiculo = ?", (id_vehiculo,))
    resultado=cursor.fetchone()
    cursor.close()
    conn.close()
    return resultado

def obtener_detalles_visitante(id_persona):
    conn = sqlite3.connect(bd_name)
    cursor = conn.cursor()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM visitante WHERE id_visitante = ?", (id_persona,))
    resultado=cursor.fetchone()
    cursor.close()
    conn.close()
    return resultado

def registrar_personal(dni_ayudante, nombre_ayudate, telefono_ayudante,rol,foto_personal):
    conn = sqlite3.connect(bd_name)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO personal (id_personal, nombre, telefono, rol, foto_personal) VALUES (?,?,?,?,?)",
                   (dni_ayudante, nombre_ayudate, telefono_ayudante, rol,foto_personal))
    conn.commit()
    cursor.close()
    conn.close() 

def registrar_vehiculo(id_vehiculo,sede,foto_vehiculo):
    conn = sqlite3.connect(bd_name)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO vehiculo (id_vehiculo, sede, foto_vehiculo) VALUES (?,?,?)",(id_vehiculo,sede,foto_vehiculo))
    conn.commit()
    cursor.close()
    conn.close() 

def registrar_visitante(id_visitante,empresa):
    conn = sqlite3.connect(bd_name)
    cursor = conn.cursor()
    sql="INSERT INTO visitante (id_visitante,empresa) VALUES (?,?)"
    cursor.execute(sql,(id_visitante,empresa))
    conn.commit()
    cursor.close()
    conn.close()

def registrar_visita_visitante_tbl(id_visitante,tipo,area,motivo_visita,quien_autoriza,sede,observacion,fecha_hora):
    conn = sqlite3.connect(bd_name)
    cursor = conn.cursor()
    sql="INSERT INTO registros_visitante (id_visitante,tipo,area,motivo_visita,quien_autoriza,sede,observacion,fecha_registro) VALUES (?,?,?,?,?,?,?,?)"
    time.sleep(0.2)
    cursor.execute(sql,(id_visitante,tipo,area,motivo_visita,quien_autoriza,sede,observacion,fecha_hora))
    conn.commit()
    cursor.close()
    conn.close()
    
# Actualizaciones
def update_foto_vehiculo(id_vehiculo, foto):
    conn = sqlite3.connect(bd_name)
    cursor = conn.cursor()
    sql = "UPDATE vehiculo SET foto_vehiculo = ? WHERE id_vehiculo = ?"
    cursor.execute(sql, (foto, id_vehiculo))
    conn.commit()
    cursor.close()
    conn.close()

def update_foto_personal(id_persona,foto):
    conn = sqlite3.connect(bd_name)
    cursor = conn.cursor()
    sql = "UPDATE personal SET foto_personal = ? WHERE id_personal = ?"
    cursor.execute(sql, (foto, id_persona))
    conn.commit()
    cursor.close()
    conn.close()

def update_telefono_foto_personal(id_persona,telefono,foto):
    conn = sqlite3.connect(bd_name)
    cursor = conn.cursor()
    sql = "UPDATE personal SET telefono = ?, foto_personal = ? WHERE id_personal = ?"
    cursor.execute(sql, (telefono, foto, id_persona))
    conn.commit()
    cursor.close()
    conn.close()

def update_telefono_personal(id_persona,telefono):
    conn = sqlite3.connect(bd_name)
    cursor = conn.cursor()
    sql = "UPDATE personal SET telefono = ? WHERE id_personal = ?"
    cursor.execute(sql, (telefono,id_persona))
    conn.commit()
    cursor.close()
    conn.close()

