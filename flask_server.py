from flask import Flask, request, render_template, session, redirect, url_for, jsonify
from flask_login import LoginManager,login_required, login_user,UserMixin
###from flask_socketio import SocketIO, emit, join_room, leave_room
from datetime import datetime
import pytz
from tablas import obtener_datos_entrada_salida_diccionario,arreglo_ua_de_datos_entrada_salida,obtener_datos_entrada_salida_visitante_diccionario,arreglo_ua_de_datos_entrada_salida_visitante
import time
import io
from PIL import Image
import base64 #Para codificar las fotos y mandar a las plantillas
from conexiones_db import validar_usuario,registrar_e_s_vehiculos,obtener_detalles_persona, obtener_imagen_persona,obtener_detalle_vehiculo,obtener_imagen_vehiculo,obtener_detalles_visitante,registrar_personal,registrar_vehiculo,registrar_visitante,registrar_visita_visitante_tbl,update_foto_vehiculo,update_foto_personal,update_telefono_foto_personal,update_telefono_personal

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'DstxDFrwfMmtFUHFO1A5bwhESwpED29SjMnehPstabYVDGI41idF'
#socketio = SocketIO(app)
#=================================Configuración de Logeo=============================
# Configurar Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'iniciar_sesion'
# Simular un modelo de usuario
class User(UserMixin):
    def __init__(self, user_id, username, password):
        self.id = user_id
        self.username = username
        self.password = password
# Función para obtener un usuario de la base de datos por nombre de usuario
def get_user(id_user):
    resultado=validar_usuario(id_user)[0:3]
    if resultado:
        user_id,username, password = resultado
        return User(user_id, username, password)
    else:
        return None

@login_manager.user_loader
def load_user(id_user):
    resultado=validar_usuario(id_user)[0:3]
    if resultado:
        user_id, username, password = resultado
        return User(user_id, username, password)
    else:
        return None        
# Definir una función de manejo de errores para el error 405 (Method Not Allowed)
@app.errorhandler(405)
def method_not_allowed_error(e):
    return redirect('/')        
#=================================Configuración de Logeo=============================

def fecha_hora_registro():
    hora_peru = pytz.timezone('America/Lima')
    hora_actual_peru = datetime.now(hora_peru)
    return hora_actual_peru.strftime('%d-%m-%Y %H:%M:%S')

def codificar_foto_b64(foto_bits):
    if foto_bits:
        imagen_base64 = base64.b64encode(foto_bits).decode('utf-8')
        return imagen_base64
    else:
        return None
@app.route('/')
def login():
    return render_template('iniciar_sesion.html')

@app.route('/iniciar_sesion', methods=['POST'])
def iniciar_sesion():
    id_user = request.form['id_user'] #Codigo de validación
    usuario = request.form['usuario']
    contrasena = request.form['contrasena']
    resultado=validar_usuario(id_user)
    if resultado:
        if resultado[2] == contrasena and resultado[1] == usuario:
            user = get_user(id_user) #Es el dni de la persona o personas que harán cada rol.
            login_user(user)
            sede = resultado[4]  # Obtener la sede del resultado
            session['sede'] = sede  
            if resultado[3] == 'operador':
                # Emitir el evento para unir al operador a la sala
                ###socketio.emit('join_room', {'room': sede})
                return render_template('registros_form.html',sede=sede)
            elif resultado[3] == 'visualizador':
                # Emitir el evento para unir al visualizador a la sala
                ###socketio.emit('join_room', {'room': sede})
                return render_template('registros_e_s.html',ua=arreglo_ua_de_datos_entrada_salida(sede),sede=sede)
        else:    
            return render_template('user_pass_incorrecto.html')    
    else:
        return render_template('user_pass_incorrecto.html')

@app.route('/zona_visitantes')
@login_required
def zona_visitantes():
    return render_template('registros_e_s_visitante.html',ua=arreglo_ua_de_datos_entrada_salida_visitante())

@app.route('/zona_registros')
@login_required
def zona_registros():
    return render_template('registros_form.html',sede=session.get('sede'))

# @socketio.on('join_room')
# def handle_join_room(data):
#     room = data['room'] #Obtener el ID de la session
#     join_room(room)

# # Emitir evento de actualización de la tabla de registros en vehículos
# ###def emitir_actualizacion_a_sala_de_sede_vehiculos(sede):
#     # Obtener los nuevos datos de la tabla para la sede específica
#     nuevos_datos = obtener_datos_entrada_salida_diccionario(sede)
#     # Emitir los nuevos datos solo a la sala correspondiente a la sede
#     # socketio.emit(f'nuevos_datos_tabla_{sede}', nuevos_datos)
#     socketio.emit('nuevos_datos_tabla', nuevos_datos)

# # Emitir evento de actualización de la tabla de registros en visitantes
# ###def emitir_actualizacion_a_sala_de_sede_visitantes(sede):
#     # Obtener los nuevos datos de la tabla para la sede específica
#     nuevos_datos = obtener_datos_entrada_salida_visitante_diccionario(sede)
#     # Emitir los nuevos datos solo a la sala correspondiente a la sede
#     # socketio.emit(f'nuevos_datos_tabla_{sede}', nuevos_datos)
#     socketio.emit('nuevos_datos_tabla_visitante', nuevos_datos)

@app.route('/form_registro', methods=['POST'])
@login_required
def registro():
    if 'sede' not in session:
        return redirect(url_for('login'))
    tipo_e_s = request.form['tipo'] #Se refiere a la entrada o a la salida
    observacion = request.form['observacion'] #Observacion en el registro
    vehiculo = request.form['vehiculo'] #id_vehiculo
    conductor = request.form['conductor'] #id_conductor
    ayudante = request.form['ayudante'] #id_ayudante
    sede = session['sede']

    tipo_vehiculo = 'interno'
    if conductor == ayudante:
        registrar_e_s_vehiculos(vehiculo, conductor, '440', tipo_e_s, sede, fecha_hora_registro(), observacion)
        tipo_vehiculo ='externo'
    else:
        registrar_e_s_vehiculos(vehiculo, conductor, ayudante, tipo_e_s, sede, fecha_hora_registro(), observacion)

    vehiculo_resultado = obtener_detalle_vehiculo(vehiculo)
    conductor_resultado = obtener_detalles_persona(conductor)
    ayudante_resultado = obtener_detalles_persona(ayudante)
    # Emitir los nuevos datos solo a la sala correspondiente a la sede del operador
    ###emitir_actualizacion_a_sala_de_sede_vehiculos(session.get('sede')) 

    flag_v=0
    flag_cond=0
    flag_ayu=0
    #Sobre los detalles obtenidos anteriormente
    if vehiculo_resultado:
        flag_v=1
    if conductor_resultado:
        flag_cond=1
    if ayudante_resultado:
        flag_ayu=1


    fv=0
    fc=0
    fa=0

    try:
        imagen_v = obtener_imagen_vehiculo(vehiculo)
        if imagen_v == (None,) or imagen_v == None: 
            fv = 0  # No hay imagen del vehículo
        else:
            fv = 1  # Hay una imagen del vehículo
    except FileNotFoundError:
        print("El archivo de imagen del vehículo no se encontró.")
        fv = 0
    except Exception as e:
        print("Error al obtener imagen del vehículo:", e)
        raise  # Re-lanza la excepción para que sea manejada en otro lugar del código si es necesario

    try:
        imagen_c = obtener_imagen_persona(conductor)
        if imagen_c == (None,) or imagen_c == None: 
            fc = 0
        else:
            fc = 1
    except FileNotFoundError:
        print("El archivo de imagen de la persona no se encontró.")
        fc = 0
    except Exception as e:
        print("Error al obtener imagen de la persona:", e)
        raise  

    try:
        imagen_a = obtener_imagen_persona(ayudante)
        if imagen_a == (None,) or imagen_a == None: 
            fa = 0
        else:
            fa = 1
    except FileNotFoundError:
        print("El archivo de imagen de la persona no se encontró.")
        fa = 0
    except Exception as e:
        print("Error al obtener imagen de la persona:", e)
        raise  

    registros_actores=[vehiculo_resultado,conductor_resultado,ayudante_resultado]
    #Se tiene que comprobar que los actores estén registrados en la base de datos

    if (not vehiculo_resultado or not conductor_resultado or not ayudante_resultado or fv==0 or fc==0 or fa==0):
        if not vehiculo_resultado:
            vehiculo_resultado=''
        if not conductor_resultado:
            conductor_resultado=''
        if not ayudante_resultado:
            ayudante_resultado=''         
        # registros_actores valida si existen registros en la base de datos
        # 'vehiculo' es lo que tiene que "meterse" en el formulario de registro por si no existiera para no repetir la tarea
        if tipo_vehiculo == 'interno':
            return render_template('registrar_actores.html', registros_actores=registros_actores,vehiculo=vehiculo,tipo_vehiculo=tipo_vehiculo,dni_conductor=conductor,dni_ayudante=ayudante,flag_v=flag_v,flag_cond=flag_cond,flag_ayu=flag_ayu,fv=fv,fc=fc,fa=fa)
        else: #Si es externo
            return render_template('registrar_actores_externo.html', registros_actores=registros_actores[0:2],vehiculo=vehiculo,tipo_vehiculo=tipo_vehiculo,dni_conductor=conductor,flag_v=flag_v,flag_cond=flag_cond,fv=fv,fc=fc)

    elif registros_actores[0]:
        foto_vehiculo_b64=codificar_foto_b64(obtener_imagen_vehiculo(vehiculo)[0])
        foto_conductor_b64=codificar_foto_b64(obtener_imagen_persona(conductor)[0])
        foto_ayudante_b64=codificar_foto_b64(obtener_imagen_persona(ayudante)[0])
        return render_template('registro_guardado_con_exito.html',report=registros_actores,foto_vehiculo_b64=foto_vehiculo_b64,foto_conductor_b64=foto_conductor_b64,foto_ayudante_b64=foto_ayudante_b64,tipo_vehiculo=tipo_vehiculo)


def transformar_foto(foto_objeto_name):
    if f'{foto_objeto_name}' in request.files:
        try:
            foto = request.files[f'{foto_objeto_name}'].read()
            imagen = Image.open(io.BytesIO(foto))
            nueva_imagen = imagen.resize((250,240)) # Ancho x Largo
            nueva_imagen_bytes = io.BytesIO()
            nueva_imagen.save(nueva_imagen_bytes, format='JPEG')
            foto = nueva_imagen_bytes.getvalue()
        except Image.UnidentifiedImageError:
            # Si no se puede identificar la imagen, asignar un valor predeterminado o nulo
            foto = None
    else:
        # Si no se proporciona foto, asignar un valor predeterminado o nulo
        foto = None
    return foto


@app.route('/registrar_actores_db', methods=['POST'])
@login_required
def registrar_actores_db():
    flag_v = request.form['flag_v']
    flag_cond = request.form['flag_cond']
    flag_ayu = request.form['flag_ayu']
    fv = request.form['fv']
    fc = request.form['fc']
    fa = request.form['fa']
    # Vehículo
    #print(request.form)
    vehiculo_placa = request.form.get('vehiculo_placa')
    vehiculo_sede = request.form.get('vehiculo_sede')
    #update_foto_vehiculo(vehiculo_placa,transformar_foto('foto_vehiculo'))
    #Conductor
    dni_conductor = request.form.get('dni_conductor')
    nombre_conductor = request.form.get('nombre_conductor')
    telefono_conductor = request.form.get('telefono_conductor')
    #Ayudante 
    dni_ayudante = request.form.get('dni_ayudante')
    telefono_ayudante = request.form.get('telefono_ayudante')
    nombre_ayudate = request.form.get('nombre_ayudate')
    #print(vehiculo_placa,vehiculo_sede,"-",dni_conductor,nombre_conductor,telefono_conductor,"-",dni_ayudante,telefono_ayudante,nombre_ayudate)

    if (flag_v =='0'):
        registrar_vehiculo(vehiculo_placa,vehiculo_sede,transformar_foto('foto_vehiculo'))
    if (flag_cond =='0'):
        registrar_personal(dni_conductor, nombre_conductor, telefono_conductor,'chofer',transformar_foto('foto_conductor')) 
    if (flag_ayu =='0'):
        registrar_personal(dni_ayudante, nombre_ayudate, telefono_ayudante,'ayudante',transformar_foto('foto_ayudante'))

    if(fv == '0'):
        update_foto_vehiculo(vehiculo_placa,transformar_foto('foto_vehiculo')) 
    if(fc == '0'):
        update_foto_personal(dni_conductor,transformar_foto('foto_conductor'))
        time.sleep(0.1)
        update_telefono_personal(dni_conductor,telefono_conductor)
    if(fa == '0'):
       update_foto_personal(dni_ayudante,transformar_foto('foto_ayudante'))
       time.sleep(0.1)
       update_telefono_personal(dni_ayudante,telefono_ayudante) 
    return render_template('guardado_exitoso.html')

@app.route('/registrar_actores_db_externo', methods=['POST'])
@login_required
def registrar_actores_db_externo():
    flag_v = request.form['flag_v']
    flag_cond = request.form['flag_cond']
    fv = request.form['fv']
    fc = request.form['fc']
    # Vehículo
    #print(request.form)
    vehiculo_placa = request.form.get('vehiculo_placa')
    vehiculo_sede = request.form.get('vehiculo_sede')
    #update_foto_vehiculo(vehiculo_placa,transformar_foto('foto_vehiculo'))
    #Conductor
    dni_conductor = request.form.get('dni_conductor')
    nombre_conductor = request.form.get('nombre_conductor')
    telefono_conductor = request.form.get('telefono_conductor')
    foto_vehiculo = request.form.get('foto_vehiculo')

    if (flag_v == '0'):
        registrar_vehiculo(vehiculo_placa,vehiculo_sede,transformar_foto(foto_vehiculo))
    if (flag_cond =='0'):
        registrar_personal(dni_conductor, nombre_conductor, telefono_conductor,'chofer',transformar_foto('foto_conductor'))
    if (flag_cond != '0'): #Actualización del número de teléfono
        update_telefono_personal(dni_conductor,telefono_conductor)
    if(fv == '0'):
        update_foto_vehiculo(vehiculo_placa,transformar_foto('foto_vehiculo')) 
    if(fc == '0'):
        update_foto_personal(dni_conductor,transformar_foto('foto_conductor')) 
 
    return render_template('guardado_exitoso.html')

@app.route('/visitante_form')
@login_required
def visitante_form():   
    return render_template('visitante_form_dni.html')

@app.route('/validar_visitante', methods=['POST'])
@login_required
def validar_visitante():
    tipo=request.form['tipo'] #Se refiere al tipo de entrada:1 y salida:0
    dni = request.form['dni']

    f_perso=0
    imagen_visitante=obtener_imagen_persona(dni)
    if imagen_visitante == (None,): 
        f_perso = 0
    else:
        f_perso = 1

    visitante_resultado = obtener_detalles_persona(dni)
    detalles_visitante = obtener_detalles_visitante(dni)
    telef=''
    if visitante_resultado:
        telef=visitante_resultado[2]
    else:
        telef=None

    ft=0 #flag telefono
    if telef==None:
        ft=0
    else:
        ft=1

    if visitante_resultado and f_perso==1: #Existe y tiene foto
        foto_personal_b64=codificar_foto_b64(imagen_visitante[0])
        if ft == 1:
            if tipo=='1': #Si es una entrada
                return render_template('registrar_visita.html',dni=dni, datos_visita=visitante_resultado,detalles_visitante=detalles_visitante,tipo=tipo,foto_personal_b64=foto_personal_b64)
            else: #Es una salida tipo=0
                return render_template('salida_registrada_visitante.html', datos_visita=visitante_resultado,detalles_visitante=detalles_visitante,foto_personal_b64=foto_personal_b64)
        if ft == 0:
            return render_template('registrar_foto_visitante.html', dni=dni, f_perso=0, datos_visita=visitante_resultado,detalles_visitante=detalles_visitante,ft=ft,ya_con_foto=1)
    else:
        if visitante_resultado and f_perso==0: #Existe y no tiene foto. Aqui se está mandando también si tiene o no n° teléfono
            return render_template('registrar_foto_visitante.html', dni=dni, f_perso=f_perso, datos_visita=visitante_resultado,detalles_visitante=detalles_visitante,ft=ft,ya_con_foto=0)
        else:
            return render_template('registrar_visitante.html', dni=dni)

@app.route('/registrar_datos_visitante', methods=['POST'])
@login_required
def registrar_datos_visitante():
    dni = request.form['dni']
    nombre_completo = request.form['nombre_completo']
    telefono_visitante = request.form['telefono_visitante']
    nombre_empresa = request.form['nombre_empresa']
    f_perso = request.form['f_perso'] #Se refiere a la foto de la persona
    ft = request.form['ft'] #Flag telefono 0=None 1!=None
    ya_con_foto  = request.form['ya_con_foto']
    if f_perso == '0':
        if ft == '0' and ya_con_foto=='0': #Si no hubiera telefono
            update_telefono_foto_personal(dni,telefono_visitante,transformar_foto('foto_visitante'))
        elif ft == '1' and ya_con_foto=='0': #Si hay un numero de telefono
            update_foto_personal(dni,transformar_foto('foto_visitante'))
        elif ft == '0' and ya_con_foto=='1':
            update_telefono_personal(dni,telefono_visitante)
    else: #f_perso=1 #Sí hay foto
        registrar_personal(dni,nombre_completo,telefono_visitante,'visitante',transformar_foto('foto_visitante'))
        time.sleep(0.2)
        registrar_visitante(dni,nombre_empresa)
    #Despues de registrar al visitante en la BD se pasa a generar el registro
    visitante_resultado = obtener_detalles_persona(dni)
    detalles_visitante = obtener_detalles_visitante(dni)
    foto_personal_b64=codificar_foto_b64(obtener_imagen_persona(dni)[0])   
    return render_template('registrar_visita.html',dni=dni,datos_visita=visitante_resultado,detalles_visitante=detalles_visitante,tipo='1',foto_personal_b64=foto_personal_b64)#Por defecto es un ingreso :: tipo=1

@app.route('/registrar_visita_visitante', methods=['POST'])
@login_required
def registrar_visita_visitante():
    dni = request.form['dni']
    tipo = request.form['tipo'] #Se refiere al ingreso o salida
    area = request.form['area']
    motivo_visita = request.form['motivo_visita']
    quien_autoriza = request.form['quien_autoriza']
    observacion = request.form['observacion']
    sede=session['sede']
    registrar_visita_visitante_tbl(dni,tipo,area,motivo_visita,quien_autoriza,sede,observacion,fecha_hora_registro())
    ###emitir_actualizacion_a_sala_de_sede_visitantes(sede)
    return redirect('/visitante_form')

@app.route('/registrar_observacion_salida', methods=['POST'])
@login_required
def registrar_observacion_salida():
    observacion = request.form['observacion']
    dni = request.form['dni']
    sede=session['sede']
    registrar_visita_visitante_tbl(dni,'0','---','---','---',sede,observacion,fecha_hora_registro())
    ###emitir_actualizacion_a_sala_de_sede_visitantes(sede)
    return redirect('/visitante_form')

@app.route('/ver_foto_vehiculo')
@login_required
def ver_foto_vehiculo():
    placa = request.args.get('placa')
    foto_vehiculo_b64=codificar_foto_b64(obtener_imagen_vehiculo(placa)[0])   
    return foto_vehiculo_b64

@app.route('/ver_foto_persona')
@login_required
def ver_foto_persona():
    dni = request.args.get('dni')
    foto_personal_b64=codificar_foto_b64(obtener_imagen_persona(dni)[0])
    return foto_personal_b64

@app.route('/cerrar_sesion')
@login_required
def cerrar_sesion():
    session.pop('sede',None)
    return redirect('/')

#*********************API SEGURIDAD*******************
@app.route('/api/tables')
#@login_required
def api_seguridad():
    # Registros de vehiculos
    password=request.args.get('tandem')
    if password=='t8YxvK2e0f4foHH5fKhBhgz8FMjIyyYyIHRYpdX0bugbJ7mHJD':
        registros=obtener_datos_entrada_salida_diccionario('api')
        return jsonify(registros)
    # Registros de visitantes
    else:
        if password=='uyzRTP3OpMfxPQbe7DUzd77fLWSzNMj6zJ2zwofRDdUf8b8FzttBBswCtbOVkhJ45XFISmjvFWa51VLv':
            registros=obtener_datos_entrada_salida_visitante_diccionario('api')
            return jsonify(registros)
        else:
            return jsonify({'Error':'401'})

#*********************API SEGURIDAD*******************


if __name__ == '__main__':
    app.run(debug=True)
    #socketio.run(app, allow_unsafe_werkzeug=True)
    #socketio.run(app, port=5001, allow_unsafe_werkzeug=True) #Para el cambio de puerto

