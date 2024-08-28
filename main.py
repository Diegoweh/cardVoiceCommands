import time

import serial

from database_operations import delete_record, insert_record, query_record
from dbConection import DBConnection
from text_to_speach import TextToSpeech
from voice_to_text import SpeechToText
from voiceVerification import VoiceVerification


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

def send_command_to_car(command, bluetooth):
    bluetooth.write(command.encode())
    time.sleep(0.1)

def close_serial_port(ser):
    ser.close()

def main():
    # Ruta del archivo de credenciales
    credentials_path = "C:/Users/diego/OneDrive/Desktop/librerias/lofty-tea-415604-8ecaca3e531b.json"
    # Crear instancia de la conexión a la base de datos
    db_conn = DBConnection(host="localhost", user="root", password="skate123", database="CRUD")
    # Inicializar objetos para conversión de texto a voz y verificación de voz
    speech_to_text = SpeechToText(credentials_path)
    tts = TextToSpeech()
    voice_verifier = VoiceVerification("recorded_audio.wav")

    # Puerto serial para la comunicación con el Arduino
    serial_port = 'COM4'
    bluetooth = connect_to_serial_port(serial_port)  # Conectar al puerto serial
    
    # Verificar si la conexión se realizó correctamente
    if bluetooth:
        while True:
            tts.speak("\nDiga un comando.")
            print("\nDiga un comando:")

            # Grabar audio
            audio_filename = "opcion_audio.wav"
            speech_to_text.record_audio(duration=3, filename=audio_filename)

            # Analizar el audio para opciones del menú
            opcion = speech_to_text.analyze_audio_for_menu_option(audio_filename, ["avanzar", "detente", "izquierda", "derecha", "salir", "reversa"])

            # Enviar el comando al Arduino a través de la conexión serial
            if opcion == "avanzar":
                send_command_to_car('F', bluetooth)
                tts.speak("avanzando...")
                print("avanzando...")
            elif opcion == "reversa":
                send_command_to_car('B', bluetooth)
                tts.speak("retrocediendo...")
                print("retrocediendo...")
            elif opcion == "detente":
                send_command_to_car('S', bluetooth)
                tts.speak("Deteniendose...")
                print("Deteniendose...")
            elif opcion == "izquierda":
                send_command_to_car('L', bluetooth)
                tts.speak("Girando a la izquierda...")
                print("Girando a la izquierda...")
            elif opcion == "derecha":
                send_command_to_car('R', bluetooth)
                tts.speak("Girando a la derecha...")
                print("Girando a la derecha...")
            elif opcion == "salir":
                tts.speak("Saliendo del programa...")
                print("Saliendo del programa...")
                break
            else:
                tts.speak("Opción no válida. Por favor, seleccione una opción válida.")
                print("Opción no válida. Por favor, seleccione una opción válida.")
        
        close_serial_port(bluetooth)  # Cerrar conexión serial al finalizar

if __name__ == "__main__":
    main()