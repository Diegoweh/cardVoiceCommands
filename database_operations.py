from dbConection import DBConnection
from text_to_speach import TextToSpeech
from voice_to_text import SpeechToText


def insert_record(db_conn, speech_to_text, tts):
    tts.speak("Por favor, dicte su nombre.")
    nombre_audio = "nombre_audio.wav"
    speech_to_text.record_audio(duration=5, filename=nombre_audio)
    nombre = speech_to_text.transcribe_audio(nombre_audio)

    tts.speak("Por favor, dicte su edad.")
    edad_audio = "edad_audio.wav"
    speech_to_text.record_audio(duration=5, filename=edad_audio)
    edad_transcrita = speech_to_text.transcribe_audio(edad_audio)

    try:
        edad = int(edad_transcrita[0])
    except ValueError:
        tts.speak("No se pudo entender la edad. Por favor, intente nuevamente.")
        print("No se pudo entender la edad. Por favor, intente nuevamente.")
        return

    query = "INSERT INTO usuarios (nombre, edad) VALUES (%s, %s)"
    values = (nombre[0], edad)
    db_conn.connect()
    cursor = db_conn.connection.cursor()
    cursor.execute(query, values)
    db_conn.connection.commit()
    tts.speak("Registro insertado correctamente.")
    print("Registro insertado correctamente.")
    db_conn.disconnect()

def delete_record(db_conn, speech_to_text, tts):
    tts.speak("Por favor, dicte el nombre del registro que desea borrar.")
    nombre_audio = "nombre_audio.wav"
    speech_to_text.record_audio(duration=5, filename=nombre_audio)
    nombre = speech_to_text.transcribe_audio(nombre_audio)

    query = "DELETE FROM usuarios WHERE nombre = %s"
    values = (nombre[0],)
    db_conn.connect()
    cursor = db_conn.connection.cursor()
    cursor.execute(query, values)
    db_conn.connection.commit()
    deleted_rows = cursor.rowcount
    if deleted_rows > 0:
        tts.speak("Registro borrado correctamente.")
        print("Registro borrado correctamente.")
    else:
        tts.speak("No se encontró ningún registro con ese nombre o ya ha sido eliminado.")
        print("No se encontró ningún registro con ese nombre o ya ha sido eliminado.")
    db_conn.disconnect()

def query_record(db_conn, speech_to_text, tts):
    tts.speak("Por favor, dicte su nombre.")
    nombre_audio = "nombre_audio.wav"
    speech_to_text.record_audio(duration=5, filename=nombre_audio)
    nombre = speech_to_text.transcribe_audio(nombre_audio)

    query = "SELECT nombre, edad FROM usuarios WHERE nombre = %s"
    values = (nombre[0],)
    db_conn.connect()
    cursor = db_conn.connection.cursor()
    cursor.execute(query, values)
    result = cursor.fetchone()
    db_conn.disconnect()

    if result:
        tts.speak(f"El registro encontrado es de {result[0]} y tiene {result[1]} años.")
        print(f"Nombre: {result[0]}, Edad: {result[1]}")
    else:
        tts.speak("No se encontró ningún registro con ese nombre.")
        print("No se encontró ningún registro con ese nombre.")
