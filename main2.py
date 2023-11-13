import serial #para que se ejecute este módulo, debe escribir en la venta de simbolo del sistema o cmd lo siguiente: pip install pyserial
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
from data1 import Cancha, Usuario, base_de_datos, canchas

ventana = tk.Tk()
ventana.title("Polideportivo")

dni_entry = None  # Variable global para el Entry de DNI
consulta_label = None  # Variable global para la etiqueta de consulta
# Configuración de la comunicación serial
#puerto_serial = serial.Serial('COM9', 9600)  # Ajusta el puerto COM según tu configuración


def obtener_fecha_hora_actual():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def reservar_cancha(usuario):
      # Envía el comando de reserva a Arduino
    #puerto_serial.write(b'reservar')

    # Lee la respuesta de Arduino
    #respuesta_arduino = puerto_serial.readline().decode('utf-8').strip()

    #if respuesta_arduino == 'reserva_exitosa':
      #  cancha_reservada = puerto_serial.readline().decode('utf-8').strip()
       # usuario.reserva = cancha_reservada
       # usuario.numero_cancha_reservada = cancha_reservada.numero
        #usuario.fecha_hora_reserva = obtener_fecha_hora_actual()
        #consulta_label.config(text=f"Cancha reservada: {cancha_reservada.tipo} (Número {cancha_reservada.numero}) para el {usuario.fecha_hora_reserva}")
        #return True
    #elif respuesta_arduino == 'sin_canchas_disponibles':
      #  consulta_label.config(text="No hay canchas disponibles en este momento.")
     #   return False
    #canchas_disponibles = [cancha for cancha in canchas if not cancha.reservada]
    #if usuario.reserva and usuario.fecha_hora_reserva.date() == datetime.now().date():
     #   consulta_label.config(text=f"Ya tiene una reserva para hoy: {usuario.reserva.tipo} (Número {usuario.reserva.numero}) a las {usuario.fecha_hora_reserva.strftime('%H:%M:%S')}")
    #    return False

    canchas_disponibles = [cancha for cancha in canchas if not cancha.reservada]
    
    if canchas_disponibles:
        cancha_reservada = canchas_disponibles[0]
        usuario.reserva = cancha_reservada
        usuario.numero_cancha_reservada = cancha_reservada.numero
        usuario.fecha_hora_reserva = obtener_fecha_hora_actual()
        cancha_reservada.reservada = True
        consulta_label.config(text=f"Cancha reservada: {cancha_reservada.tipo} (Número {cancha_reservada.numero}) para el {usuario.fecha_hora_reserva}")
        return True
    else:
        consulta_label.config(text="No hay canchas disponibles en este momento.")
        return False

def ingresar_cancha(usuario):
    if usuario.reserva and usuario.reserva.reservada:
        tiempo_actual = datetime.now()
        tiempo_reserva = datetime.strptime(usuario.fecha_hora_reserva, "%d/%m/%Y %H:%M:%S")
        diferencia_tiempo = tiempo_actual - tiempo_reserva

        if diferencia_tiempo <= timedelta(minutes=10):
            consulta_label.config(text=f"Acceso permitido a la cancha {usuario.reserva.numero} de {usuario.reserva.tipo} para {usuario.nombre}")
        else:
            consulta_label.config(text=f"Acceso denegado. Reserva expirada para la cancha {usuario.reserva.numero} de {usuario.reserva.tipo} para {usuario.nombre}")
            usuario.reserva.reservada = False
            usuario.reserva = None
    else:
        consulta_label.config(text=f"Acceso denegado. No tiene reserva en este momento para {usuario.nombre}.")

def realizar_reserva():
    global consulta_label
    dni = dni_entry.get()
    if dni in base_de_datos:
        usuario = base_de_datos[dni]
        if not usuario.reserva:
            if reservar_cancha(usuario):
                if not consulta_label:
                    consulta_label = tk.Label(ventana, text="")
                    consulta_label.pack()
                consulta_label.config(text=f"Cancha reservada: {usuario.reserva.tipo} (Número {usuario.reserva.numero}) para el {usuario.fecha_hora_reserva}")
            else:
                consulta_label.config(text="No hay canchas disponibles en este momento.")
        else:
            consulta_label.config(text="Ya tiene una reserva.")
    else:
        consulta_label.config(text="Usuario no encontrado en la base de datos.")

def main():
    global dni_entry
    dni_label = tk.Label(ventana, text="Ingrese su DNI:")
    dni_label.pack()

    dni_entry = tk.Entry(ventana)
    dni_entry.pack()

    reserva_button = tk.Button(ventana, text="Realizar Reserva", command=realizar_reserva)
    reserva_button.pack()

    acceso_button = tk.Button(ventana, text="Ingresar a la Cancha", command=lambda: ingresar_cancha(base_de_datos[dni_entry.get()]))
    acceso_button.pack()

    global consulta_label
    consulta_label = tk.Label(ventana, text="")
    consulta_label.pack()
# Al final, cierra el puerto serial cuando se cierre la ventana
#ventana.protocol("WM_DELETE_WINDOW", lambda: cerrar_serial(ventana))

#def cerrar_serial(ventana):
    # Cierra el puerto serial antes de cerrar la ventana
   # puerto_serial.close()
    #ventana.destroy()

    ventana.mainloop()


if __name__ == "__main__":
    main()


