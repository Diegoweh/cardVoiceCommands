import time

import serial


def delay(ms):
    time.sleep(ms / 1000.0)

def connect_to_serial_port(port_number):
    ser = serial.Serial()
    ser.baudrate = 9600
    ser.port = port_number
    ser.rtscts = True
    ser.dtr = True
    ser.open()
    if ser.is_open:
        print(f"CONECTADO AL PUERTO: {ser.port}")
        return ser
    else:
        print("ERROR")
        return None

def send_command(ser, command):
    ser.write(command.encode() + b'\r')

def close_serial_port(ser):
    ser.close()

def read_serial_data(ser):
    return ser.read(ser.in_waiting).decode()

# Cambiar 'COM12' al número de puerto correcto
serial_port = 'COM4'

ser = connect_to_serial_port(serial_port)

# Ejemplo de cómo usar las funciones definidas arriba
if ser:
    while True:
        command = input("Ingrese un comando (A/B para ejemplo): ")
        send_command(ser, command)
        if command.lower() == 'exit':
            break
        response = read_serial_data(ser)
        print("Respuesta recibida:", response)

    close_serial_port(ser)
